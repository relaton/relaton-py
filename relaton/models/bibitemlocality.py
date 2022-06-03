from typing import Optional, List

from pydantic.dataclasses import dataclass

from relaton.models import GenericStringValue


@dataclass
class BibItemLocality:
    """Bibliographic item locality."""

    type: str
    reference_from: GenericStringValue
    reference_to: Optional[GenericStringValue] = None


@dataclass
class Locality(BibItemLocality):
    pass


@dataclass
class LocalityStack:
    locality: List[Locality]
