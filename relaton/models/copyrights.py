from typing import TypedDict, Optional, Union, List

from pydantic.dataclasses import dataclass


__all__ = ('Copyright', )

from .orgs import Organization
from .people import Person


# Pydantic dataclasses don’t actually support aliases, contrary to docs
Copyright = TypedDict('Copyright', {
    'from': int,
    'owner': List[Union[Organization, Person]],
})
