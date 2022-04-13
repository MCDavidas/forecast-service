import uvicorn
from fastapi import FastAPI

from routers import forecast_router

app = FastAPI()
app.include_router(forecast_router.router)


if __name__ == '__main__':
    uvicorn.run("app:app", port=1111, host='127.0.0.1')
