import aiohttp
from datetime import date, datetime
from statistics import mean
from geopy.geocoders import Nominatim

from settings import API_KEY


LOCATOR = Nominatim(user_agent="weather-forecast-application")


async def get_weather(region: str, start_date: date, end_date: date):
    location = LOCATOR.geocode(region)
    complete_url = (
        f'https://api.openweathermap.org/data/2.5/onecall?lat={location.latitude}&lon={location.longitude}'
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
        return None, None, None
