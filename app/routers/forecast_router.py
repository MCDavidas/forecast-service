from datetime import date, timedelta
from decimal import Decimal
from enum import Enum

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse

from db.dals.forecast_dal import ForecastDAL
from utils.weather_api import get_weather_future, get_weather_history, get_location
from dependencies import get_forecast_dal


class ForecastQuery(BaseModel):
    region: str
    start_date: date
    end_date: date


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


router = APIRouter()


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(forecast_query: ForecastQuery):
    if not date.today() <= forecast_query.start_date <= forecast_query.end_date:
        return JSONResponse(
            status_code=422,
            content={'detail': [{'loc': ['body'], "msg": "incorrect period"}]},
        )

    la, lo = get_location(forecast_query.region)
    if not la or not lo:
        return JSONResponse(
            status_code=422,
            content={'detail': [{'loc': ['body', 'region'], "msg": "incorrect region"}]},
        )

    stats = await get_weather_future(la, lo, forecast_query.start_date, forecast_query.end_date)
    if not stats:
        return JSONResponse(
            status_code=204,
            content={'detail': [{'loc': ['body'], "msg": "no forecast for specified period"}]},
        )

    item = {
        'region': forecast_query.region,
        'start_date': forecast_query.start_date,
        'end_date': forecast_query.end_date,
        'average_daytime_temperature': stats[0],
        'average_nighttime_temperature': stats[1],
        'average_humidity': stats[2],
    }
    return item


@router.get("/statisctics/{period}", response_model=ForecastResponse)
async def generate_statisctics(period: Period,
                               forecast_query: ForecastHistory,
                               forecast_dal: ForecastDAL = Depends(get_forecast_dal)):
    if period == Period.week:
        days_count = 7
    if period == Period.month:
        days_count = 30
    if period == Period.year:
        days_count = 365

    la, lo = get_location(forecast_query.region)
    if not la or not lo:
        return JSONResponse(
            status_code=422,
            content={'detail': [{'loc': ['body', 'region'], "msg": "incorrect region"}]},
        )

    stats = await get_weather_history(forecast_dal, forecast_query.region, la, lo, days_count)
    item = {
        'region': forecast_query.region,
        'start_date': date.today() - timedelta(days=days_count),
        'end_date': date.today(),
        'average_daytime_temperature': stats[0],
        'average_nighttime_temperature': stats[1],
        'average_humidity': stats[2],
    }
    return item
