from db.config import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Numeric,
)


class Forecast(Base):
    __tablename__ = 'forecast'

    id = Column(Integer, primary_key=True)
    region = Column(String, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    average_daytime_temperature = Column(Numeric)
    average_nighttime_temperature = Column(Numeric)
    average_humidity = Column(Integer)
