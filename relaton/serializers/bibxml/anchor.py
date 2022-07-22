from typing import List
from string import ascii_letters, digits
import re

from ...models.bibdata import BibliographicItem, DocID
from ...util import as_list


__all__ = (
    'get_suitable_anchor',
    'to_valid_xsid',
    'XSID_REGEX',
    'XSID_ILLEGAL',
)


def get_suitable_anchor(item: BibliographicItem) -> str:
    """From a :class:`~relaton.models.bibdata.BibliographicItem` instance
    get best anchor value and return it as a string.

    :param item: a :class:`bib_models.bibdata.BibliographicItem` instance
    :returns str: a string to be used as anchor
    :rtype: str
    :raises ValueError: unable to obtain an anchor, e.g. item has no docids
    """

    docids: List[DocID] = as_list(item.docid or [])

    try:
        anchor_docid: DocID = (
            # Prefer primary
            [d for d in docids if d.primary]
            # Fallback case (docid.scope may be going away)
            or [d for d in docids if getattr(d, 'scope', '') == 'anchor']
            # Otherwise, take any docid
            or docids)[0]
    except IndexError:
        raise ValueError("No suitable anchor could be determined")
    else:
        if XSID_REGEX.match(anchor_docid.id) is not None:
            return anchor_docid.id
        else:
            return to_valid_xsid(anchor_docid.id)


def to_valid_xsid(val: str) -> str:
    """
    Transforms a string into a valid xs:id value.
    Transformation is lossy and irreversible.
    """
    return XSID_ILLEGAL.sub('', re.sub(
        r'^\d',
        r'_\g<0>',
        re.sub(
            r'[-\s]+',
            '_',
            val
            .replace('/', '-')
            .replace(':', '.')
            .strip('-_')
        )
    ))


XSID_REGEX = re.compile(r'^[a-zA-Z_][-.\w]*$')
"""A regular expression matching a full valid xs:id value."""

XSID_ILLEGAL = re.compile(r'[^-.\w]')
"""A regular expression matching xs:id characters that are invalid
anywhere within an xs:id string."""
