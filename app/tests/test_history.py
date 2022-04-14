import pytest
import os
import asyncio
from requests import Response

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app import app
from dependencies import get_forecast_dal
from initialize import init_db
from db.dals.forecast_dal import ForecastDAL


engine = create_async_engine("sqlite+aiosqlite:///./test.db", future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

client = TestClient(app)


async def override_get_forecast_dal():
    async with async_session() as session:
        async with session.begin():
            yield ForecastDAL(session)


app.dependency_overrides[get_forecast_dal] = override_get_forecast_dal


@pytest.fixture(scope="module")
def event_loop():
    from db.declaration import Base

    loop = asyncio.new_event_loop()
    loop.run_until_complete(init_db(engine, Base))
    yield loop
    loop.close()
    os.remove('./test.db')


def assert_correct_output(response: Response, region: str):
    assert response.status_code == 200

    content = response.json()
    assert 'start_date' in content
    assert 'end_date' in content
    assert 'average_daytime_temperature' in content
    assert 'average_nighttime_temperature' in content
    assert 'average_humidity' in content
    assert content['region'] == region


def test_get_history_week(event_loop):
    body = {
        'region': 'Moscow',
        }

    response = client.get('/statisctics/week', json=body)
    assert_correct_output(response, body['region'])


def test_get_history_month(event_loop):
    body = {
        'region': 'London',
        }

    response = client.get('/statisctics/month', json=body)
    assert_correct_output(response, body['region'])


def test_get_history_year(event_loop):
    body = {
        'region': 'Paris',
        }

    response = client.get('/statisctics/year', json=body)
    assert_correct_output(response, body['region'])


def test_get_history_typo(event_loop):
    body = {
        'region': 'Paris',
        }

    response = client.get('/statisctics/wek', json=body)
    assert response.status_code == 422


def test_get_history_incorrect_region(event_loop):
    body = {
        'region': 'S2kjSK&%%@@',
        }

    response = client.get('/statisctics/month', json=body)
    assert response.status_code == 422
    for message in response.json()['detail']:
        assert message['loc'] == ['body', 'region']
        assert message['msg'] == 'incorrect region'
