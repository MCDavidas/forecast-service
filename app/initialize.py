import asyncio


async def init_db(engine, base):
    # create db tables
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)


if __name__ == '__main__':
    from db.config import engine
    from db.declaration import Base
    from db.models.forecast import Forecast

    asyncio.run(init_db(engine, Base))
