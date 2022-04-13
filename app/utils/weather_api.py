import asyncio
import typing as tp
import aiohttp
import time
from datetime import date, datetime, timedelta
from decimal import Decimal
from statistics import mean
from geopy.geocoders import Nominatim

from settings import API_KEY
from db.dals.forecast_dal import ForecastDAL


LOCATOR = Nominatim(user_agent="weather-forecast-application")


def get_location(region: str):
    location = LOCATOR.geocode(region)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


async def get_weather_future(la: float, lo: float, start_date: date, end_date: date):
    complete_url = (
        f'https://api.openweathermap.org/data/2.5/onecall?lat={la}&lon={lo}'
        f'&exclude=current,minutely,hourly,alerts&units=metric&appid={API_KEY}'
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(complete_url) as resp:
            week_forecast = await resp.json()

    days = [day for day in week_forecast['daily']
            if end_date >= datetime.fromtimestamp(day['dt']).date() >= start_date]

    if days:
        average_daytime_temperature = mean([day['temp']['day'] for day in days])
        average_nighttime_temperature = mean([day['temp']['night'] for day in days])
        average_humidity = sum([day['humidity'] for day in days]) // len(days)
        return average_daytime_temperature, average_nighttime_temperature, average_humidity
    else:
        return None


async def request_history(la: float, lo: float, stamp: int):
    complete_url = (
        f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={la}&lon={lo}'
        f'&dt={stamp}&units=metric&appid={API_KEY}'
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(complete_url) as resp:
            history = await resp.json()

    day = history['hourly']

    daytime_temperature = mean([Decimal(hour['temp']) for hour in day[5:-1]])
    nighttime_temperature = mean([Decimal(hour['temp']) for hour in day[:5] + day[-1:]])
    humidity = sum([hour['humidity'] for hour in day]) // 24

    return daytime_temperature, nighttime_temperature, humidity


async def get_weather_history(forecast_dal: ForecastDAL, region: str, days_count: int):
    average_daytime_temperature: Decimal = Decimal(0)
    average_nighttime_temperature: Decimal = Decimal(0)
    average_humidity: Decimal = Decimal(0)
    five_day_forecast: tp.List[tp.List[tp.Any]] = []

    base = date.today()
    for x in range(days_count):
        day = base - timedelta(days=x)
        forecast = await forecast_dal.get_forecast_by_date(day)
        if forecast:
            average_daytime_temperature += forecast.daytime_temperature
            average_nighttime_temperature += forecast.nighttime_temperature
            average_humidity += forecast.humidity
        else:
            if not five_day_forecast:
                location = LOCATOR.geocode(region)
                timestamps = [time.mktime(x.timetuple()) for x in [base - timedelta(days=x) for x in range(5)]]
                five_day_forecast = await asyncio.gather(
                    *[request_history(location.latitude, location.longitude, int(stamp)) for stamp in timestamps]
                    )

            forecast = five_day_forecast[x % 5]
            await forecast_dal.create_forecast(region=region,
                                               date=day,
                                               daytime_temperature=forecast[0],
                                               nighttime_temperature=forecast[1],
                                               humidity=forecast[2])
            average_daytime_temperature += forecast[0]
            average_nighttime_temperature += forecast[1]
            average_humidity += forecast[2]

    average_daytime_temperature /= days_count
    average_nighttime_temperature /= days_count
    average_humidity //= days_count

    return average_daytime_temperature, average_nighttime_temperature, average_humidity
