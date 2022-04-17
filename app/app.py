import uvicorn
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor

from routers import forecast_router
from settings import IP_ADDRESS, PORT

app = FastAPI()
app.include_router(forecast_router.router)


@app.on_event("startup")
async def on_startup():
    app.state.executor = ProcessPoolExecutor(max_workers=3)


@app.on_event("shutdown")
async def on_shutdown():
    app.state.executor.shutdown()


if __name__ == '__main__':
    uvicorn.run("app:app", port=PORT, host=IP_ADDRESS)
