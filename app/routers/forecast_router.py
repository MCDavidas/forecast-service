from datetime import date
from decimal import Decimal

from fastapi import APIRouter
from pydantic import BaseModel

from db.models.forecast import Forecast
from utils.weather_api import get_weather


class ForecastQuery(BaseModel):
    region: str
    start_date: date
    end_date: date


class ForecastResponse(ForecastQuery):
    average_daytime_temperature: Decimal
    average_nighttime_temperature: Decimal
    average_humidity: int


router = APIRouter()


# @router.get("/forecasts")
# async def get_all_books(forecast_dal: ForecastDAL = Depends(get_forecast_dal)) -> List[Forecast]:
#     return await forecast_dal.get_all_forecasts()


@router.get("/forecast", response_model=ForecastResponse)
async def get_forecast(forecast_query: ForecastQuery) -> Forecast:
    stats = await get_weather(forecast_query.region, forecast_query.start_date, forecast_query.end_date)
    item = {
        'region': forecast_query.region,
        'start_date': forecast_query.start_date,
        'end_date': forecast_query.end_date,
        'average_daytime_temperature': stats[0],
        'average_nighttime_temperature': stats[1],
        'average_humidity': stats[2],
    }
    return item
