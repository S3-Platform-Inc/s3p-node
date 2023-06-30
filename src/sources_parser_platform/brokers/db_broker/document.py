import asyncio

from sqlalchemy import text

from src.sources_parser_platform.types import SPP_document
from .main import sync_get_engine


class Document:

    @classmethod
    def all_by_source_name(cls, source_name: str) -> list[SPP_document]:
        """
        Безопасное получение данные об источнике. В случае, если в базе данных нет записи об источнике, он добавится.
        :param source_name:
        :type source_name:
        :return:
        :rtype:
        """
        documents: list[tuple] = asyncio.run(Document.__get_all_by_source(source_name))
        res: list[SPP_document] = []
        for row in documents:
            res.append(SPP_document(
                doc_id=row[0],
                title=row[1],
                abstract=row[2],
                text=row[3],
                web_link=row[4],
                local_link=row[5],
                other_data=row[6],
                pub_date=row[7],
                load_date=row[8],
            ))
        return res

    @classmethod
    def safe_init(cls, source_name: str, document: SPP_document) -> bool:
        """

        :param source_name:
        :type source_name:
        :param document:
        :type document:
        :return:
        :rtype:
        """
        res = asyncio.run(Document.__init_document(source_name, document))
        return res[0][0]

    @classmethod
    def safe_update(cls, source_name: str, *args) -> bool:
        """
        Безопасное обновление или добавление данных о документе.
        :param source_name:
        :type source_name:
        :param args:
        :type args:
        :return:
        :rtype:
        """
        ...

    @classmethod
    async def __init_document(cls, source_name: str, __document: SPP_document):
        async with sync_get_engine().execution_options(isolation_level='AUTOCOMMIT').begin() as conn:
            query_param = f"SELECT * FROM public.safe_init_document(null,'{source_name}', '{__document.title}'" \
                          f", '{__document.abstract}', '{__document.web_link}', '{__document.pub_date}');"
            result = await conn.execute(text(query_param))
            await conn.commit()

        return result.fetchall()

    @classmethod
    async def __get_all_by_source(cls, source_name: str):
        """
        Анисхронное безопасное получение всех документов одного источника по его имени
        :param source_name:
        :type source_name:
        :return:
        :rtype:
        """
        async with sync_get_engine().execution_options(isolation_level='AUTOCOMMIT').begin() as conn:
            query_param = f"SELECT * FROM public.get_all_documents_by_source(null, '{source_name}');"
            result = await conn.execute(text(query_param))
            await conn.commit()

        return result.fetchall()


if __name__ == "__main__":
    aas = Document.all_by_source_name('pci')
    print(aas)
