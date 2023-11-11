"""Model for job objects."""

import re
from datetime import datetime, timedelta
from typing import Optional, Union

from pydantic import BaseModel, field_validator


def clean_numeric_string(value: Union[str, None]) -> Optional[str]:
    """Clean a string, extracting numerical values."""
    if isinstance(value, str):
        return "".join(filter(str.isdigit, value))
    return None


def validate_client_spendings(value: Union[str, None]) -> Union[str, None]:
    """Validate the client spendings field."""
    if isinstance(value, str):
        value = re.sub(r"[^\d.Kk]", "", value)
        if "K" in value or "k" in value:
            value = value.replace("K", "").replace("k", "")
            return str(float(value) * 1000)
        return str(value)
    return value


def validate_posted_on(value: Union[str, None]) -> Union[str, None]:
    """Validate the posted_on field."""
    if isinstance(value, str):
        time_units = {
            "days": "days",
            "day": "days",
            "minutes": "minutes",
            "minute": "minutes",
            "hours": "hours",
            "hour": "hours",
        }
        match = re.match(r"(\d+) (\w+) ago", value)
        if match and match.groups()[1] in time_units:
            unit = time_units[match.groups()[1]]
            if unit in ("days", "minutes", "hours"):
                return (
                    datetime.now()
                    - timedelta(**{unit: int(match.groups()[0])})
                ).isoformat()
    return value


class JobSection(BaseModel):
    """A Pydantic BaseModel representing a job section."""

    title: str
    link: str
    description: str
    skills: list
    proposals: str
    posted_on: str
    country: str
    budget: Optional[str] = None
    job_type: Optional[str] = None
    duration: Optional[str] = None
    experience: Optional[str] = None
    payment_verified: Optional[bool] = False
    client_spendings: Optional[str] = None

    @field_validator("client_spendings")
    def validate_client_spendings(cls, v):
        """Validate the client spendings field."""
        return validate_client_spendings(v)

    @field_validator("budget")
    def extract_numerical_value(cls, v):
        """Extract the numerical value from the budget string."""
        return clean_numeric_string(v)

    @field_validator("posted_on")
    def validate_posted_on(cls, v):
        """Validate the posted_on field."""
        return validate_posted_on(v)
