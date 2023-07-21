from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

# url = URL.create(
#     drivername="postgresql",
#     username='postgres',
#     host='localhost',
#     port=32768,
#     database='sourceParserPlatform'
# )
DRIVERNAME = "postgresql"
USERNAME = 'sppuser'
HOST = 'localhost'
PORT = 8888
DATABASE = 'sourceParserPlatform'
PASSWORD = 'spppassword'

url = f"{DRIVERNAME}+asyncpg://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

async_engine = create_async_engine(url, echo=True)


async def get_async_engine() -> AsyncEngine:
    while True:
        yield create_async_engine(url, echo=True)


def sync_get_engine() -> AsyncEngine:
    return create_async_engine(url, echo=True)
