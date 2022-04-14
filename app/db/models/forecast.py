from db.declaration import Base
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
    date = Column(Date)
    daytime_temperature = Column(Numeric)
    nighttime_temperature = Column(Numeric)
    humidity = Column(Integer)
