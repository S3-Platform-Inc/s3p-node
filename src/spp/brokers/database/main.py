import os

import psycopg2

USERNAME = os.getenv('DB_USER')
HOST = os.getenv('DB_DOCKER_HOST')
PORT = os.getenv('DB_DOCKER_PORT')
DATABASE = os.getenv('DB_DATABASE')
PASSWORD = os.getenv('DB_PASSWORD')


def psConnection():
    """
    Create a connection to the PostgreSQL Control-database by psycopg2
    :return:
    """
    return psycopg2.connect(
        database=DATABASE,
        user=USERNAME,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )


def interval(param: str | None) -> str | None:
    """
    Function that wrapped interval parameter for SQL query
    :param param:
    :return:
    """
    if param:
        return f"'{param}'::interval"
    else:
        return None
