from typing import Optional, Union, List

from pydantic.dataclasses import dataclass

from .contacts import ContactMethod


__all__ = ('Organization', )


@dataclass
class Organization:
    """Describes an organization."""

    name: Union[List[str], str]
    contact: Optional[List[ContactMethod]] = None
    url: Optional[str] = None
    abbreviation: Optional[str] = None
