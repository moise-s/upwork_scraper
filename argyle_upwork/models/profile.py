import re

from pydantic import BaseModel, field_validator


class ProfilePage(BaseModel):
    """A Pydantic BaseModel representing a profile section."""

    title: str
    hourly_rate: str
    description: str
    skills: list
    employment_history: list

    @field_validator("hourly_rate")
    def clean_hourly_rate(cls, value):
        """Extract the numerical value from the hourly rate string."""
        if isinstance(value, str):
            return value.replace("$", "").replace("/hr", "").strip()
        return value

    @field_validator("skills")
    def strip_whitespace_skills(cls, value):
        """Strip leading and trailing whitespaces for each skill in the list."""
        if isinstance(value, list):
            return [skill.strip() for skill in value]
        return value

    @field_validator("employment_history")
    def strip_whitespace_employment_history(cls, value):
        """Strip leading and trailing whitespaces for each employment history entry."""
        if isinstance(value, list):
            cleaned_employment_history = []
            for entry in value:
                cleaned_entry = {
                    "title": entry.get("title", "").strip(),
                    "period": re.sub(
                        r"\s+", " ", entry.get("period", "")
                    ).strip(),
                }
                cleaned_employment_history.append(cleaned_entry)
            return cleaned_employment_history
        return value


class AccountSection(BaseModel):
    """A Pydantic BaseModel representing a account section."""

    user_id: str
    user_name: str
    user_masked_email: str

    @field_validator("user_name")
    def strip_whitespace(cls, value):
        """Strip leading and trailing whitespaces and collapse consecutive spaces."""
        if isinstance(value, str):
            return " ".join(value.split())
        return value


class LocationSection(BaseModel):
    """A Pydantic BaseModel representing a contact section."""

    adress_street: str
    adress_street_2: str
    address_city: str
    address_state: str
    address_zip: str
    address_country: str
    phone: str

    @field_validator("phone")
    def strip_whitespace(cls, value):
        """Strip leading and trailing whitespaces and collapse consecutive spaces."""
        if isinstance(value, str):
            return "+" + "".join(c for c in value if c.isdigit())
        return value

    @field_validator("address_zip")
    def convert_empty_string_to_none(cls, value):
        """Convert empty string to None."""
        if value == "":
            return None
        return value

    @field_validator("address_state")
    def clean_address_state(cls, value):
        """Remove leading and trailing whitespaces and a comma."""
        if isinstance(value, str):
            return value.strip(", ").strip()
        return value


class Profile(BaseModel):
    account_session: AccountSection
    location_session: LocationSection
    profile_page: ProfilePage
