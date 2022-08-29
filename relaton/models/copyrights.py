from typing import TypedDict, Optional, Union, List

from pydantic.dataclasses import dataclass


__all__ = ('CopyrightOwner', 'Copyright', )

from .strings import GenericStringValue


@dataclass
class CopyrightOwner:
    """Who or which organization holds the copyright.
    """
    name: Union[List[GenericStringValue], GenericStringValue]
    url: Optional[str] = None
    abbreviation: Optional[GenericStringValue] = None


# Pydantic dataclasses don’t actually support aliases, contrary to docs
Copyright = TypedDict('Copyright', {
    'from': int,
    'owner': Union[List[CopyrightOwner]],
})
