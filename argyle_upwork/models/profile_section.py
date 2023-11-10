import re
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, field_validator


class ProfileSection(BaseModel):
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
                    "period": re.sub(r'\s+', ' ', entry.get("period", "")).strip()
                }
                cleaned_employment_history.append(cleaned_entry)
            return cleaned_employment_history
        return value