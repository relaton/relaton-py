from typing import Optional, Union, List

from pydantic.dataclasses import dataclass

from .contacts import ContactMethod
from .strings import GenericStringValue

__all__ = ('Organization', )


@dataclass
class Organization:
    """Describes an organization."""

    name: Union[List[GenericStringValue], GenericStringValue]
    contact: Optional[List[ContactMethod]] = None
    url: Optional[str] = None
    abbreviation: Optional[GenericStringValue] = None
