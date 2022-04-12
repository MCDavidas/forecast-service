from typing import List
from datetime import date
from decimal import Decimal

from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.forecast import Forecast


class ForecastDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_forecast(self,
                              region: str,
                              start_date: date,
                              end_date: date,
                              average_daytime_temperature: Decimal,
                              average_nighttime_temperature: Decimal,
                              average_humidity: int):
        new_forecast = Forecast(region=region,
                                start_date=start_date,
                                end_date=end_date,
                                average_daytime_temperature=average_daytime_temperature,
                                average_nighttime_temperature=average_nighttime_temperature,
                                average_humidity=average_humidity)
        self.db_session.add(new_forecast)
        await self.db_session.flush()

    async def get_all_forecasts(self) -> List[Forecast]:
        q = await self.db_session.execute(select(Forecast).order_by(Forecast.id))
        forecasts: List[Forecast]
        forecasts = q.scalars().all()
        return forecasts

    '''
    async def update_forecast(self,
                              book_id: int,
                              name: Optional[str],
                              author: Optional[str],
                              release_year: Optional[int]):
        q = update(Forecast).where(Forecast.id == book_id)
        if name:
            q = q.values(name=name)
        if author:
            q = q.values(author=author)
        if release_year:
            q = q.values(release_year=release_year)
        q.execution_options(synchronize_session="fetch")
        await  self.db_session.execute(q)
    '''
