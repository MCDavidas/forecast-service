from typing import List
from datetime import date
from decimal import Decimal

from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from db.models.forecast import Forecast


class ForecastDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_forecast(self,
                              region: str,
                              date: date,
                              daytime_temperature: Decimal,
                              nighttime_temperature: Decimal,
                              humidity: int):
        new_forecast = Forecast(region=region,
                                date=date,
                                daytime_temperature=daytime_temperature,
                                nighttime_temperature=nighttime_temperature,
                                humidity=humidity)
        self.db_session.add(new_forecast)
        await self.db_session.flush()

    async def get_all_forecasts(self) -> List[Forecast]:
        q = await self.db_session.execute(select(Forecast).order_by(Forecast.id))
        forecasts: List[Forecast]
        forecasts = q.scalars().all()
        return forecasts

    async def get_forecast(self, region: str, date: date) -> Forecast:
        query = select(Forecast).where(Forecast.date == date).where(Forecast.region == region)
        results = await self.db_session.execute(query)
        try:
            (result,) = results.one()
        except NoResultFound:
            result = None
        return result
