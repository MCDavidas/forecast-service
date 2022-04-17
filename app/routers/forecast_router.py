import asyncio
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from db.dals.forecast_dal import ForecastDAL
from entities.forecast_entities import (
    ForecastResponse,
    ForecastHistory,
    ForecastQuery,
    Period,
)
from utils.weather_api import get_weather_future, get_weather_history, get_location
from dependencies import get_forecast_dal


router = APIRouter()


async def run_in_process(executor, fn, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, fn, *args)  # wait and return result


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(forecast_query: ForecastQuery,
                       request: Request) -> ForecastResponse:
    if not date.today() <= forecast_query.start_date:
        return JSONResponse(
            status_code=422,
            content={'detail': [{'loc': ['body'], "msg": "incorrect period"}]},
            )

    la, lo = await run_in_process(request.app.state.executor, get_location, forecast_query.region)
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

    item = ForecastResponse(**{
        'region': forecast_query.region,
        'start_date': forecast_query.start_date,
        'end_date': forecast_query.end_date,
        'average_daytime_temperature': stats[0],
        'average_nighttime_temperature': stats[1],
        'average_humidity': stats[2],
    })
    return item


@router.get("/statisctics/{period}", response_model=ForecastResponse)
async def generate_statisctics(request: Request,
                               period: Period,
                               forecast_query: ForecastHistory,
                               forecast_dal: ForecastDAL = Depends(get_forecast_dal)) -> ForecastResponse:
    if period == Period.week:
        days_count = 7
    if period == Period.month:
        days_count = 30
    if period == Period.year:
        days_count = 365

    la, lo = await run_in_process(request.app.state.executor, get_location, forecast_query.region)
    if not la or not lo:
        return JSONResponse(
            status_code=422,
            content={'detail': [{'loc': ['body', 'region'], "msg": "incorrect region"}]},
        )

    stats = await get_weather_history(forecast_dal, forecast_query.region, la, lo, days_count)
    item = ForecastResponse(**{
        'region': forecast_query.region,
        'start_date': date.today() - timedelta(days=days_count),
        'end_date': date.today(),
        'average_daytime_temperature': stats[0],
        'average_nighttime_temperature': stats[1],
        'average_humidity': stats[2],
    })
    return item
