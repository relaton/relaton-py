"""
Some of Relaton models implemented as Pydantic models.
"""

# NOTE: Docstrings for dataclasses and models below
# may be used when rendering OpenAPI schemas,
# where ReSTructuredText syntax is not
# supported. Stick to plain text.

from __future__ import annotations

# Required for circular dependency
# between BibliographicItem and Relation.

from typing import List, Union, Optional
import datetime

from pydantic import BaseModel, Extra, validator
from pydantic.dataclasses import dataclass

from .bibitemlocality import LocalityStack, Locality
from .copyrights import Copyright
from .strings import Title, GenericStringValue
from .people import Person
from .orgs import Organization
from .links import Link
from .dates import Date, validate_relaxed_date


__all__ = (
    'DocID',
    'BibliographicItem',
    'Relation',
    'Contributor',
    'Series',
    'BiblioNote',
)


@dataclass
class DocID:
    """Typed :term:`document identifier`.

    May be given by publisher or issued by some third-party system.
    """

    id: str

    type: str
    """:term:`document identifier type`.
    Determines the format of the ``id`` field.
    """

    primary: Optional[bool] = None
    """If ``True``, this identifier is considered
    a :term:`primary document identifier`.
    """

    scope: Optional[str] = None
    """
    .. todo:: Clarify the meaning of scope.
    """


@dataclass
class BiblioNote:
    """Bibliographic note."""

    content: str
    """Note content."""

    type: Optional[str] = None
    """The class of the note associated with the bibliographic item.
    May be used to differentiate rendering of notes in bibliographies.
    """


class Series(BaseModel):
    """
    A series that given document belongs to.

    Note: formattedref is exclusive with other properties.
    """
    # TODO: Don’t make all properties optional, use union types or something

    formattedref: Optional[Union[GenericStringValue, str]] = None
    """References a bibliographic item via a primary ID.
    Exclusive with other properties.
    """

    title: Optional[Union[
        GenericStringValue,
        List[GenericStringValue]]] = None
    abbrev: Optional[str] = None
    place: Optional[str] = None
    number: Optional[str] = None
    organization: Optional[str] = None
    run: Optional[str] = None
    partnumber: Optional[str] = None
    type: Optional[str] = 'main'


@dataclass
class Role:
    type: Optional[str] = None
    """See ``ContributorRoleType``."""

    description: Optional[List[GenericStringValue]] = None


@dataclass
class Contributor:
    """Anyone who helped create or publish the document.

    .. important:: This is equivalent of ``ContributionInfo`` model in LutaML;
                   ``Contributor`` itself is defined as a union of
                   ``Person`` or ``Organization`` in LutaML.
    """

    role: List[Role]
    person: Optional[Person] = None
    organization: Optional[Organization] = None


@dataclass
class Edition:
    content: str
    number: Optional[str] = None


@dataclass
class VersionInfo:
    """Describes a version. Could be used for drafts."""

    draft: Optional[str] = None
    """Draft version."""

    # revdate: Optional[Union[str, datetime.date]] = None
    # """Revision date (format not clear)"""


class BibliographicItem(BaseModel, extra=Extra.allow):
    """
    Relaton’s primary entity, bibliographic item.

    Note: formattedref is exclusive with other properties.
    In some contexts (such as relations) bibliographic item can be specified
    as a “pointer”, which callers can resolve to full metadata.
    formattedref is that pointer.
    It is expected to have a shape of a primary docid.
    """

    # TODO: Don’t make all optional, use union types or something
    # if Relaton spec makes it clear which properties
    # are mandatory in absence of formattedref.

    formattedref: Optional[GenericStringValue] = None
    """A human-readable string representing this bibliographic item
    in a not strongly specified way.
    """

    docid: List[DocID]
    """A list of identifiers. The only required property."""

    docnumber: Optional[str] = None
    language: Optional[Union[List[str], str]] = None
    type: Optional[str] = None
    doctype: Optional[str] = None
    script: Optional[Union[List[str], str]] = None
    date: Optional[Union[List[Date], Date]] = None
    link: Optional[Union[List[Link], Link]] = None

    relation: 'Optional[List[Relation]]' = None

    version: Optional[List[VersionInfo]] = None

    title: Optional[Union[List[Title], Title]] = None
    edition: Optional[Edition] = None
    abstract: Optional[Union[List[GenericStringValue], GenericStringValue]] = \
        None

    fetched: Optional[datetime.date] = None
    revdate: Optional[Union[str, datetime.date, List[Union[str, datetime.date]]]] = None

    biblionote: Optional[Union[List[BiblioNote], BiblioNote]] = None

    contributor: Optional[List[Contributor]] = None

    place: Optional[Union[List[str], str]] = None

    series: Optional[List[Series]] = None

    keyword: Optional[Union[List[str], str]] = None

    copyright: Optional[Union[List[Copyright], Copyright]] = None

    extent: Optional[Union[LocalityStack, Locality]] = None

    @validator('revdate', pre=True)
    def validate_revdate(cls, v, **kwargs):
        """Validates ``revdate``, allowing it to be unspecific."""
        if isinstance(v, list):
            # TODO: Could this be handled with ``each_item`` keyword instead?
            return [
                validate_relaxed_date(i)
                for i in v
                if i
            ]
        return validate_relaxed_date(v, optional=True)


class Relation(BaseModel, extra=Extra.allow):
    """
    Indicates a relationship from given bibliographic item to another.
    """
    type: str
    """Describes the relationship."""

    bibitem: BibliographicItem
    """Relationship target."""

    description: Optional[GenericStringValue]
    """Describes the relationship in more detail."""


BibliographicItem.update_forward_refs()
