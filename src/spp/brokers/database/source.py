import asyncio

from sqlalchemy import text

from spp.types import SPP_source
from .main import sync_get_engine


class Source:
    """
    Схема источника для взаимодействия с базой данных.
    """

    @staticmethod
    def safe(source_name: str) -> SPP_source:
        """
        Безопасное получение данные об источнике. В случае, если в базе данных нет записи об источнике, он добавится.
        :param source_name:
        :_type source_name:
        :return:
        :rtype:
        """
        res = asyncio.run(Source.__safe_init(source_name))
        return SPP_source(*res[0])

    @staticmethod
    def safe_update(source_name: str, *args) -> SPP_source:
        """
        Безопасное обновление или добавление данных об источнике.
        :param source_name:
        :_type source_name:
        :param args:
        :_type args:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    async def __safe_init(source_name: str):
        """
        Анисхронное безопасное получение информации об источнике по его имени
        :param source_name:
        :_type source_name:
        :return:
        :rtype:
        """
        async with sync_get_engine().begin() as conn:
            query_param = """SELECT * FROM public.safe_get_source('""" + source_name + """');"""
            result = await conn.execute(text(query_param))
            await conn.commit()
        return result.fetchall()


if __name__ == "__main__":
    aas = Source.safe('pci')
    print(aas, aas.name)
