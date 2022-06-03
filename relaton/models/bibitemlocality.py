from typing import Optional, List

from pydantic.dataclasses import dataclass

from relaton.models import GenericStringValue


@dataclass
class BibItemLocality:
    """
    The extent or location of a bibliographic item being referred to.

    A sequence of locality elements is meant to indicate hierarchical ordering,
    from greater to smaller.

    [example]
    Chapter, then page, then paragraph.

    A discontinuous range can be represented by using two adjacent localities
    with the same type.
    """

    type: str
    reference_from: GenericStringValue
    reference_to: Optional[GenericStringValue] = None


@dataclass
class Locality(BibItemLocality):
    pass


@dataclass
class LocalityStack:
    locality: List[Locality]
