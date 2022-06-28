from typing import Optional, List

from pydantic.dataclasses import dataclass


__all__ = (
    'Address',
    'ContactMethod',
    'Phone',
)


@dataclass
class Phone:
    type: Optional[str] = None
    content: str


@dataclass
class Address:
    """Address information for a contact."""

    street: Optional[List[str]] = None
    city: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None


@dataclass
class ContactMethod:
    """Address information for a person
    or organization."""
    address: Optional[Address] = None
    phone: Optional[Phone] = None
    email: Optional[str] = None
    uri: Optional[str] = None
