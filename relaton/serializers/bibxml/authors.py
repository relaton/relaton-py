from typing import List, Optional
from xml.etree.ElementTree import Element
from lxml import objectify

from ...util import as_list
from ...models.bibdata import Contributor
from ...models.orgs import Organization
from ...models.people import PersonAffiliation
from ...models.contacts import Contact
from ...models.strings import GenericStringValue


__all__ = (
  'create_author',
  'is_author',
  'AUTHOR_ROLES',
)


E = objectify.E


AUTHOR_ROLES = set(('author', 'editor', 'publisher'))
"""Relaton contributor roles that represent xml2rfc authors."""


is_author = (
    lambda contrib:
    len(set(as_list(contrib.role or [])) & AUTHOR_ROLES) > 0
)
"""Returns ``True`` if given Relaton contributor instance
represents an author in xml2rfc domain."""


def create_author(contributor: Contributor) -> Element:
    if not is_author(contributor):
        raise ValueError(
            "Unable to construct <author>: incompatible roles")

    if not contributor.organization and not contributor.person:
        raise ValueError(
            "Unable to construct <author>: "
            "neither an organization nor a person")

    author_el = E.author()

    roles = as_list(contributor.role)

    if 'editor' in roles:
        author_el.set('role', 'editor')

    org: Optional[Organization] = None
    if contributor.organization:
        org = contributor.organization
    elif contributor.person:
        affiliations: List[PersonAffiliation] = \
            as_list(contributor.person.affiliation or [])
        if len(affiliations) > 0:
            org = affiliations[0].organization
        else:
            org = None

    if org is not None:
        # Organization
        org_el = E.organization(as_list(org.name)[0])

        if org.abbreviation:
            org_el.set('abbrev', org.abbreviation)

        author_el.append(org_el)

        # Address & postal
        contacts: List[Contact] = as_list(org.contact or [])
        postal_contacts = [
            c for c in contacts
            if c.country
        ]
        if len(postal_contacts) > 0 or org.url:
            addr = E.address()

            if len(postal_contacts) > 0:
                contact = postal_contacts[0]
                postal = E.postal(
                    E.country(contact.country)
                )
                if contact.city:
                    postal.append(E.city(contact.city))
                addr.append(postal)

            if org.url:
                addr.append(E.uri(org.url))

            author_el.append(addr)

    if contributor.person:
        name = contributor.person.name
        if name.completename:
            author_el.set('fullname', name.completename.content)
        if name.surname:
            author_el.set('surname', name.surname.content)
        if name.initial:
            initials: List[GenericStringValue] = \
                as_list(name.initial or [])
            author_el.set('initials', ' '.join([
                i.content.replace('.', ' ').strip()
                for i in initials
            ]))

    return author_el
