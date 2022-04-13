from db.config import async_session
from db.dals.forecast_dal import ForecastDAL


async def get_forecast_dal():
    async with async_session() as session:
        async with session.begin():
            yield ForecastDAL(session)
