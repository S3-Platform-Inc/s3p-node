import datetime
import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

DRIVERNAME = os.getenv('DB_DRIVERNAME')
USERNAME = os.getenv('DB_USER')
HOST = os.getenv('DB_DOCKER_HOST')
PORT = os.getenv('DB_DOCKER_PORT')
DATABASE = os.getenv('DB_DATABASE')
PASSWORD = os.getenv('DB_PASSWORD')

url = f"{DRIVERNAME}+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


# async_engine = create_async_engine(url, echo=True)


# async def get_async_engine() -> AsyncEngine:
#     while True:
#         yield create_async_engine(url, echo=True)


def sync_get_engine() -> AsyncEngine:
    return create_async_engine(url, echo=False)


def _def_null_param(param) -> str:
    return param if param else "Null"


def _text_param(param: str) -> str:
    if param:
        if str(param).lower() == "null":
            return param
        else:
            return f"'{param}'"
    else:
        return "Null"


def _datetime_param(param: datetime.datetime | None) -> str | None:
    if param:
        return f"TIMESTAMP {_text_param(str(param))}"
    else:
        return None


def _interval_param(param: str | None) -> str | None:
    if param:
        return f"{_text_param(param)}::interval"
    else:
        return None
