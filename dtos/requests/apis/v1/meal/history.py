"""
DTO for fetch meal history request payload, with validation for date fields.
"""
from datetime import date
from pydantic import field_validator, Field
from typing import Optional

from dtos.requests.abstraction import IRequestDTO


class FetchMealHistoryRequestDTO(IRequestDTO):
    """
    DTO for fetch meal history request.
    Fields:
        from_date (date): Start date for history (validated).
        to_date (date): End date for history (validated).
    """
    from_date: Optional[date] = Field(default=date.today())
    to_date: Optional[date] = Field(default=date.today())

    @field_validator('from_date', 'to_date')
    @classmethod
    def validate_dates(cls, v, info):
        if not v:
            raise ValueError(f"{info.field_name} is required.")
        if not isinstance(v, date):
            raise ValueError(f"{info.field_name} must be a valid date.")
        return v

    @field_validator('to_date')
    @classmethod
    def validate_date_range(cls, v, info):
        from_date = info.data.get('from_date') if info.data else None
        if from_date and v < from_date:
            raise ValueError('to_date cannot be before from_date.')
        if v > date.today():
            raise ValueError('to_date cannot be in the future.')
        return v
