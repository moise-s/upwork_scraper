import re
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel, field_validator


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
