import re
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, field_validator


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
    def _validate_client_spendings(cls, v):
        """Validate the client spendings field."""
        if isinstance(v, str):
            v = re.sub(r"[^\d.Kk]", "", v)
            if "K" in v or "k" in v:
                v = v.replace("K", "").replace("k", "")
                return str(float(v) * 1000)
            return str(v)
        return v

    @field_validator("budget")
    def _extract_numerical_value(cls, v):
        """Extract the numerical value from the budget field."""
        if isinstance(v, str):
            v = "".join(filter(str.isdigit, v))
            return v
        return None

    @field_validator("posted_on")
    def _validate_posted_on(cls, v):
        """Validate the posted_on field."""
        if isinstance(v, str):
            time_units = {
                "days": "days",
                "day": "days",
                "minutes": "minutes",
                "minute": "minutes",
                "hours": "hours",
                "hour": "hours",
            }
            match = re.match(r"(\d+) (\w+) ago", v)
            if match and match.groups()[1] in time_units:
                unit = time_units[match.groups()[1]]
                if unit in ("days", "minutes", "hours"):
                    return (
                        datetime.now()
                        - timedelta(**{unit: int(match.groups()[0])})
                    ).isoformat()
        return v
