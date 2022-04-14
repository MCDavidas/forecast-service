Build container:
docker-compose build --no-cache

Test web-service:
docker run --rm -t -e API_KEY=676de08e92211f3ed6f9e7810725e4d1 forecastservice_web pytest

Run application:
docker-compose up

Swagger on http://127.0.0.1:8000/docs

Initialize database (execute while docker-compose is running):
docker-compose exec web python3 initialize.py

.env example:
POSTGRES_USER=forecast
POSTGRES_PASSWORD=forecast
POSTGRES_DB=forecast
API_KEY=676de08e92211f3ed6f9e7810725e4d1
