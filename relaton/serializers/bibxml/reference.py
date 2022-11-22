from typing import List, Tuple, Optional, Union, cast
import datetime
from lxml.etree import _Element
from lxml import objectify

from ...models.bibitemlocality import LocalityStack, Locality
from ...util import as_list
from ...models.bibdata import BibliographicItem, Contributor, Series
from ...models.dates import Date, parse_relaxed_date
from ...models.strings import Title, GenericStringValue

from .series import DOCID_SERIES_EXTRACTORS
from .authors import create_author, is_author
from .abstracts import create_abstract
from .target import get_suitable_target
from .anchor import get_suitable_anchor


__all__ = (
    'create_reference',
    'create_referencegroup',
)


E = objectify.E


default_title = "[title unavailable]"


def create_referencegroup(items: List[BibliographicItem]) -> _Element:
    return E.referencegroup(*(
        create_reference(item)
        for item in items
    ))


def create_reference(item: BibliographicItem) -> _Element:
    main_title: str
    if item.title:
        main_title = as_list(item.title)[0].content or default_title
    else:
        main_title = default_title

    contributors: List[Contributor] = as_list(item.contributor or [])
    author_contributors: List[Contributor] = [
        contrib
        for contrib in contributors
        if is_author(contrib)
    ]

    front = E.front(
        E.title(main_title),
        *(create_author(contrib) for contrib in author_contributors)
        if author_contributors
        else E.author(),
    )

    # IANA entries should not include any date element
    if not any(link_type.content.startswith("http://www.iana.org") for link_type in as_list(item.link or [])):
        # Publication date… Or at least any date
        published_date: Optional[datetime.date] = None
        published_date_raw: Optional[Union[str, datetime.date]] = None
        all_dates: List[Date] = as_list(item.date or [])
        specificity: Optional[str] = None
        for date in all_dates:
            if date.type == 'published':
                published_date_raw = date.value
                break
        if not published_date_raw and all_dates:
            published_date_raw = all_dates[0].value

        if published_date_raw:
            if isinstance(published_date_raw, str):
                relaxed = parse_relaxed_date(published_date_raw)
                if relaxed:
                    published_date = relaxed[0]
                    specificity = relaxed[2]
            else:
                published_date = published_date_raw
                specificity = 'day'

        if published_date and specificity:
            date_el = E.date(year=published_date.strftime('%Y'))
            if specificity in ['month', 'day']:
                date_el.set('month', published_date.strftime('%B'))
            if specificity == 'day':
                date_el.set('day', str(published_date.day))
            front.append(date_el)

    # Abstract
    abstracts: List[GenericStringValue] = as_list(item.abstract or [])
    if len(abstracts) > 0:
        front.append(create_abstract(abstracts))

    ref = E.reference(front)

    if (item.extent and (refcontent := build_refcontent_string(item.extent))):
        ref.append(E.refcontent(refcontent))

    # Series
    series: List[Optional[Tuple[str, str]]] = []
    actual_series: List[Series] = as_list(item.series or [])
    series.extend([
        (cast(List[Title], as_list(s.title or []))[0].content, s.number)
        for s in actual_series
        if s.number and s.title
    ])
    for docid in (item.docid or []):
        series.extend([
            func(docid)
            for func in DOCID_SERIES_EXTRACTORS
        ])
    for series_info in list(dict.fromkeys(series)):
        if series_info is not None:
            ref.append(E.seriesInfo(
                name=series_info[0],
                value=series_info[1],
            ))

    try:
        target = get_suitable_target(as_list(item.link or []))
    except ValueError:
        pass
    else:
        ref.append(E.format(
            type="TXT",
            target=target,
        ))

    # Anchor, may be overwritten by callers
    try:
        anchor = get_suitable_anchor(item)
    except ValueError:
        pass
    else:
        ref.set('anchor', anchor)

    return ref


def build_refcontent_string(extent: LocalityStack | Locality) -> str:
    """
    Given either :class:`~relaton.models.bibitemlocality.LocalityStack`
    or :class:`~relaton.models.bibitemlocality.Locality` instance,
    constructs a string representation of bibliographic locality
    that is suitable to be used as ``refcontent`` element contents.
    """

    parts = []

    if isinstance(extent, LocalityStack):
        for locality in extent.locality:
            if locality.type == 'container-title':
                parts.append(locality.reference_from)
            if locality.type == 'volume':
                parts.append('vol. %s' % locality.reference_from)
            elif locality.type == 'issue':
                parts.append('no. %s' % locality.reference_from)
            elif locality.type == 'page':
                parts.append('pp. %s' % locality.reference_from)
    else:
        parts.append(extent.reference_from)

    return ", ".join(parts)
