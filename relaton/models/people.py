from typing import Optional, Union, List

from pydantic.dataclasses import dataclass

from .contacts import ContactMethod
from .orgs import Organization
from .strings import GenericStringValue

__all__ = ('Forename', 'Person', 'FullName', 'GivenName', 'PersonAffiliation', )


@dataclass
class Forename(GenericStringValue):
    """A forename of a person"""

    initial: Optional[str] = None
    """
    An individual initial of the person, corresponding to the given forename.
    Does not include final punctuation, but can include hyphens.
    Can be used instead of forenames,
    if ``formatted_initials`` are not provided
    (in which case each initial will be punctuated
    following local practice).
    """


@dataclass
class GivenName:
    forename: Optional[Union[
        List[Forename],
        Forename,
    ]] = None
    """Also known as given name or first name."""

    formatted_initials: Optional[GenericStringValue] = None
    """The initials of the person, as a formatted string, including punctuation, dropping
       punctuation as desired, and including hyphens where necessary. For example,
       the initial set for Jean-Paul would be J, P; the formatted initials would be "J.-P."
       or "J-P.". Can be used instead of forenames.
    """


@dataclass
class FullName:
    """Describes a person’s name."""

    prefix: Optional[GenericStringValue] = None
    """Name prefix."""

    given: Optional[GivenName] = None

    surname: Optional[GenericStringValue] = None
    """Also known as last name or family name."""

    completename: Optional[GenericStringValue] = None
    """Full name.
    Expected to be mutually exclusive with other properties.
    """

    addition: Optional[GenericStringValue] = None
    """Addition to the name."""


@dataclass
class PersonAffiliation:
    """Affiliation of a person."""
    organization: Organization


@dataclass
class Person:
    """Describes a person."""

    name: FullName

    affiliation: Optional[Union[
        List[PersonAffiliation],
        PersonAffiliation,
    ]] = None

    contact: Optional[List[ContactMethod]] = None
    """Contact information."""
