"""Model for profile objects."""

import re
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


def clean_string(value: Union[str, None], *remove_chars: str) -> Union[str, None]:
    """Remove specified characters and strip whitespaces from a string."""
    if isinstance(value, str):
        for char in remove_chars:
            value = value.replace(char, "")
        return value.strip()
    return value


def strip_whitespace(value: Union[str, None]) -> Union[str, None]:
    """Strip leading and trailing whitespaces and collapse consecutive spaces."""
    if isinstance(value, str):
        return " ".join(value.split())
    return value


def convert_empty_string_to_none(value: str) -> Union[str, None]:
    """Convert empty string to None."""
    return None if value == "" else value


class ProfilePage(BaseModel):
    """A Pydantic BaseModel representing a profile page."""

    title: Optional[str]
    hourly_rate: Optional[str]
    description: Optional[str]
    skills: Optional[List[str]]
    employment_history: Optional[List[dict]]

    @field_validator("hourly_rate")
    def clean_hourly_rate(cls, value):
        """Extract the numerical value from the hourly rate string."""
        return clean_string(value, "$", "/hr")

    @field_validator("skills")
    def strip_whitespace_skills(cls, value):
        """Strip leading and trailing whitespaces for each skill in the list."""
        return [strip_whitespace(skill) for skill in value]

    @field_validator("employment_history")
    def strip_whitespace_employment_history(cls, value):
        """Strip leading and trailing whitespaces for each employment history entry."""
        return [
            {
                "title": strip_whitespace(entry.get("title", "")),
                "period": re.sub(r"\s+", " ", entry.get("period", "")).strip(),
            }
            for entry in value
        ]


class AccountSection(BaseModel):
    """A Pydantic BaseModel representing an account section."""

    user_id: str
    user_name: str
    user_masked_email: str

    @field_validator("user_name")
    def strip_whitespace(cls, value):
        """Strip leading and trailing whitespaces and collapse consecutive spaces."""
        return strip_whitespace(value)


class LocationSection(BaseModel):
    """A Pydantic BaseModel representing a location section."""

    address_street: Optional[str]
    address_street_2: Optional[str]
    address_city: Optional[str]
    address_state: Optional[str]
    address_zip: Optional[str]
    address_country: Optional[str]
    phone: Optional[str]

    @field_validator("phone")
    def strip_whitespace(cls, value):
        """Strip leading and trailing whitespaces and collapse consecutive spaces."""
        return "+" + "".join(c for c in value if c.isdigit())

    @field_validator("address_zip")
    def convert_empty_string_to_none(cls, value):
        """Convert empty string to None."""
        return convert_empty_string_to_none(value)

    @field_validator("address_state")
    def clean_address_state(cls, value):
        """Remove leading and trailing whitespaces and a comma."""
        return clean_string(value, ",").strip()


class Profile(BaseModel):
    """A Pydantic BaseModel representing all profile objects scanned."""

    account_session: AccountSection
    location_session: LocationSection
    profile_page: ProfilePage
