import uvicorn
from fastapi import FastAPI

from routers import forecast_router
from settings import IP_ADDRESS, PORT

app = FastAPI()
app.include_router(forecast_router.router)


if __name__ == '__main__':
    uvicorn.run("app:app", port=PORT, host=IP_ADDRESS)
