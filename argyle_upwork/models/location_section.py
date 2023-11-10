import re
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, field_validator


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
