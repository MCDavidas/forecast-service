from datetime import date, timedelta

from app import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_get_forecast():
    base = date.today()
    body = {
        'region': 'Moscow',
        'start_date': base.strftime('%Y-%m-%d'),
        'end_date': (base + timedelta(days=3)).strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 200

    content = response.json()
    assert 'average_daytime_temperature' in content
    assert 'average_nighttime_temperature' in content
    assert 'average_humidity' in content

    del content['average_daytime_temperature']
    del content['average_nighttime_temperature']
    del content['average_humidity']
    assert content == body


def test_get_forecast_no_body():
    response = client.get("/forecast")
    assert response.status_code == 422
    message = response.json()['detail'][0]
    assert message['loc'] == ['body']
    assert message['msg'] == 'field required'


def test_get_forecast_no_body_slash():
    response = client.get("/forecast/")
    assert response.status_code == 422
    message = response.json()['detail'][0]
    assert message['loc'] == ['body']
    assert message['msg'] == 'field required'


def test_get_forecast_typos():
    response = client.get("/forecasts")
    assert response.status_code == 404


def test_get_forecast_dummy_content():
    response = client.get("/forecast", data={'bla': 'bla'})
    assert response.status_code == 422
    message = response.json()['detail'][0]
    assert message['loc'] == ['body']
    assert message['msg'] == 'value is not a valid dict'


def test_get_forecast_no_region():
    base = date.today()
    body = {
        'start_date': base.strftime('%Y-%m-%d'),
        'end_date': (base + timedelta(days=3)).strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 422
    for message in response.json()['detail']:
        assert message['loc'] == ['body', 'region']
        assert message['msg'] == 'field required'


def test_get_forecast_region_int():
    base = date.today()
    body = {
        'region': 23,
        'start_date': base.strftime('%Y-%m-%d'),
        'end_date': (base + timedelta(days=3)).strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 422
    for message in response.json()['detail']:
        assert message['loc'] == ['body', 'region']
        assert message['msg'] == 'field required'


def test_get_forecast_no_start_date():
    base = date.today()
    body = {
        'region': 'Telaviv',
        'end_date': (base + timedelta(days=3)).strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 422
    for message in response.json()['detail']:
        assert message['loc'] == ['body', 'start_date']
        assert message['msg'] == 'field required'


def test_get_forecast_start_date_int():
    base = date.today()
    body = {
        'region': 'Moscow',
        'start_date': 14,
        'end_date': (base + timedelta(days=3)).strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 422
    for message in response.json()['detail']:
        assert message['loc'] == ['body', 'start_date']
        assert message['msg'] == 'field required'


def test_get_forecast_past_date():
    base = date.today()
    body = {
        'region': 'Moscow',
        'start_date': (base - timedelta(days=3)).strftime('%Y-%m-%d'),
        'end_date': (base - timedelta(days=1)).strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 400


def test_get_forecast_incorrect_period():
    base = date.today()
    body = {
        'region': 'Moscow',
        'start_date': (base + timedelta(days=3)).strftime('%Y-%m-%d'),
        'end_date': base.strftime('%Y-%m-%d'),
        }

    response = client.get("/forecast", json=body)
    assert response.status_code == 400
