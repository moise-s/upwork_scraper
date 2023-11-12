"""Model for profile objects."""

import re
from typing import List, Optional, Union

import pycountry
from pydantic import BaseModel, field_validator, model_validator


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

    job_title: Optional[str]
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

    full_name: str
    first_name: Optional[str]
    last_name: Optional[str]
    id: str
    masked_email: str

    @field_validator("full_name")
    def strip_whitespace(cls, value):
        """Strip leading and trailing whitespaces and collapse consecutive spaces."""
        return strip_whitespace(value)

    @model_validator(mode="before")
    def process_full_name(cls, values):
        """Process full_name and populate first_name and last_name."""
        full_name = values.get("full_name")
        if full_name:
            names = full_name.split()
            values["first_name"] = names[0] if names else None
            values["last_name"] = names[-1] if len(names) > 1 else None
        return values


class LocationSection(BaseModel):
    """A Pydantic BaseModel representing a location section."""

    line_1: Optional[str]
    line_2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]
    phone_number: Optional[str]

    @field_validator("phone_number")
    def validate_phone_number(cls, value):
        """Strip leading and trailing whitespaces and collapse consecutive spaces."""
        return "+" + "".join(c for c in value if c.isdigit())

    @field_validator("postal_code")
    def convert_empty_string_to_none(cls, value):
        """Convert empty string to None."""
        return convert_empty_string_to_none(value)

    @field_validator("state")
    def clean_address_state(cls, value):
        """Remove leading and trailing whitespaces and a comma."""
        return clean_string(value, ",").strip()

    @field_validator("country")
    def validate_country(cls, value):
        """Validate country and convert it to ISO 3166-1 alpha-2 format."""
        try:
            country_code = pycountry.countries.get(name=value).alpha_2
            return country_code
        except AttributeError:
            return None


class Profile(BaseModel):
    """A Pydantic BaseModel representing all profile objects scanned."""

    account_session: AccountSection
    location_session: LocationSection
    profile_page: ProfilePage
