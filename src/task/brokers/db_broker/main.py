import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

DRIVERNAME = os.getenv('DB_DRIVERNAME')
USERNAME = os.getenv('DB_USER')
HOST = os.getenv('DB_DOCKER_HOST')
PORT = os.getenv('DB_DOCKER_PORT')
DATABASE = os.getenv('DB_DATABASE')
PASSWORD = os.getenv('DB_PASSWORD')

url = f"{DRIVERNAME}+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

async_engine = create_async_engine(url, echo=True)


async def get_async_engine() -> AsyncEngine:
    while True:
        yield create_async_engine(url, echo=True)


def sync_get_engine() -> AsyncEngine:
    return create_async_engine(url, echo=False)
