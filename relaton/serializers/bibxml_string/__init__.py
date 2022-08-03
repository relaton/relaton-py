from lxml import etree
from ..types import Serializer
from ..bibxml import serialize as _original_serialize
from ...models.bibdata import BibliographicItem


__all__ = (
    'serialize',
)


def serialize(item: BibliographicItem, **kwargs) -> bytes:
    """Passes given item and any kwargs through
    to :func:`relaton.serializers.bibxml.serialize()`,
    and renders the obtained XML element as an UTF8-encoded string
    with pretty print.
    """

    # get a tree
    canonicalized_tree =  etree.fromstring(
        # obtained from a canonicalized string representation
        etree.tostring(
            # of the original bibxml tree
            _original_serialize(item, **kwargs),
            method='c14n2',
        )
        # ^ this returns a unicode string
    )

    # pretty-print that tree in utf-8 with declaration and doctype
    return etree.tostring(
        canonicalized_tree,
        encoding='utf-8',
        xml_declaration=True,
        doctype=None,
        pretty_print=True,
    )
    # ^ this returns a byte array
