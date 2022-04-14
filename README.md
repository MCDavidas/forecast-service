# Forecast service test task

FastAPI, sqlalchemy, openweathermap.org

1. Clone the project:
<code>git clone https://github.com/MCDavidas/forecast-service.git</code>

2. Build container:
<code>docker-compose build --no-cache</code>

3. Test web-service:
<code>docker run --rm -t -e API_KEY=676de08e92211f3ed6f9e7810725e4d1 forecastservice_web pytest</code>

4. Run application:
<code>docker-compose up</code>

Swagger on http://127.0.0.1:8000/docs

5. Initialize database (execute while docker-compose is running):
<code>docker-compose exec web python3 initialize.py</code>

Application receives sensitive data through environment variables. You need to create <code>.env</code> file in project root directory.

<code>.env</code> example:
```
POSTGRES_USER=forecast
POSTGRES_PASSWORD=forecast
POSTGRES_DB=forecast
API_KEY=676de08e92211f3ed6f9e7810725e4d1
```

Development took one and a half day.

I will be glad to receive any feedback :)
