from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, root_validator


class ForecastQuery(BaseModel):
    region: str
    start_date: date
    end_date: date

    @root_validator(pre=False)
    @classmethod
    def check_period(cls, values):
        a = values.get('start_date')
        b = values.get('end_date')
        if a and b and not a <= b:
            raise ValueError(message="Incorrect period")
        return values


class ForecastResponse(ForecastQuery):
    average_daytime_temperature: Decimal
    average_nighttime_temperature: Decimal
    average_humidity: int


class ForecastHistory(BaseModel):
    region: str


class Period(str, Enum):
    week = 'week'
    month = 'month'
    year = 'year'
