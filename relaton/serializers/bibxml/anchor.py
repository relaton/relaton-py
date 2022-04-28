from typing import List

from ...models.bibdata import DocID


__all__ = (
    'get_suitable_anchor',
)


def get_suitable_anchor(docids: List[DocID]):
    """From a list of :class:`~relaton.models.bibdata.DocID` instances,
    get best anchor value and return it as a string.

    Ideally it’s a ``DocID`` with ``scope`` equal to “anchor”,
    otherwise primary identifier, otherwise any idnetifier.

    :param docids: a list of :class:`bib_models.bibdata.DocID` instances
    :returns str: a string to be used as anchor
    :rtype: str
    :raises ValueError: no suitable document identifier (possibly empty list)
    """
    try:
        anchor_docid: DocID = (
            [d for d in docids if d.scope == 'anchor']
            or [d for d in docids if d.primary]
            or docids)[0]
    except IndexError:
        raise ValueError("No anchor could be found")
    else:
        return anchor_docid.id
