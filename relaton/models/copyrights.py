from typing import TypedDict, Union, List

__all__ = ('Copyright', )

from .orgs import Organization
from .people import Person


# ``from`` is reserved in Python, so if we can’t alias it we’ll just use
# a ``TypedDict`` instead of a dataclass.
# Pydantic dataclasses don’t actually support aliases, contrary to docs
Copyright = TypedDict('Copyright', {
    'from': int,
    'owner': List[Union[Organization, Person]],
})
