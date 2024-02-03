import asyncio
import json

from sqlalchemy import text
from sqlalchemy.ext.declarative import DeclarativeMeta

from src.spp.types import SPP_document, SPP_source
from .main import sync_get_engine, _def_null_param, _text_param, _datetime_param
from src.spp.utils import pack, unpack


class AlchemyEncoder(json.JSONEncoder):
    """
    Спец енкодер для перевода dict в json формат для взаимодействия с базой данных
    """

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


class Document:

    @classmethod
    def all_by_source_name(cls, source_name: str) -> list[SPP_document]:
        """
        Безопасное получение всех документов, относящихся к одному источнику
        :param source_name:
        :_type source_name:
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
                text=unpack(row[3]) if row[3] else None,
                web_link=row[4],
                local_link=row[5],
                other_data=row[6],
                pub_date=row[7],
                load_date=row[8],
            ))
        return res

    @classmethod
    def all_hashed_by_source_name(cls, source_name: str) -> list[SPP_document]:
        """
        Безопасное получение всех документов (title, web_link, pub_date), относящихся к одному источнику
        :param source_name:
        :_type source_name:
        :return:
        :rtype:
        """
        documents: list[tuple] = asyncio.run(Document.__get_all_for_hash_by_source(source_name))
        res: list[SPP_document] = []
        for row in documents:
            res.append(SPP_document(
                doc_id=row[0],
                title=row[1],
                abstract=None,
                text=None,
                web_link=row[2],
                local_link=None,
                other_data=None,
                pub_date=row[3],
                load_date=None,
            ))
        return res

    @classmethod
    def safe_init(cls, source: SPP_source, document: SPP_document) -> bool:
        """

        :param source:
        :type source:
        :param document:
        :type document:
        :return:
        :rtype:
        """
        res = asyncio.run(Document.__init_document(source, document))
        return res[0][0]

    @classmethod
    def safe_update(cls, source: SPP_source, document: SPP_document) -> bool:
        """
        Безопасное обновление или добавление данных о документе.

        Если возвращается True - то данные обновились
        Если возвращается False - то документа не было в таблице. Он был добавлен в таблицу.
        :return:
        :rtype:
        """

        res = asyncio.run(Document.__update_document(source, document))
        return res[0][0]

    @classmethod
    async def __init_document(cls, source: SPP_source, __document: SPP_document):
        source_id = source.src_id if source.src_id else None

        async with sync_get_engine().execution_options(isolation_level='AUTOCOMMIT').begin() as conn:
            query_param = f"SELECT * FROM public.safe_init_document({source_id},'{source.name}', '{__document.title}'" \
                          f", '{__document.abstract}', '{__document.web_link}', '{__document.pub_date}');"
            result = await conn.execute(text(query_param))
            await conn.commit()

        return result.fetchall()

    @classmethod
    async def __get_all_by_source(cls, source_name: str):
        """
        Анисхронное безопасное получение всех документов одного источника по его имени
        :param source_name:
        :_type source_name:
        :return:
        :rtype:
        """
        async with sync_get_engine().execution_options(isolation_level='AUTOCOMMIT').begin() as conn:
            query_param = f"SELECT * FROM public.get_all_documents_by_source(null, '{source_name}');"
            result = await conn.execute(text(query_param))
            await conn.commit()

        return result.fetchall()

    @classmethod
    async def __get_all_for_hash_by_source(cls, source_name: str):
        """
        Анисхронное безопасное получение всех документов (title, web_link, pub_date) одного источника по его имени.
        :param source_name:
        :_type source_name:
        :return:
        :rtype:
        """
        async with sync_get_engine().execution_options(isolation_level='AUTOCOMMIT').begin() as conn:
            query_param = f"SELECT * FROM public.get_all_documents_for_hash_by_source(null, '{source_name}');"
            result = await conn.execute(text(query_param))
            await conn.commit()

        return result.fetchall()

    @classmethod
    async def __update_document(cls, source: SPP_source, __document: SPP_document):
        source_id = source.src_id if source.src_id else None
        other_data = json.dumps(__document.other_data) if __document.other_data else None
        packed_text = pack(__document.text) if __document.text else None

        async with sync_get_engine().execution_options(isolation_level='AUTOCOMMIT').begin() as conn:
            query_param = f"SELECT * FROM public.safe_update_document({source_id},'{source.name}'," \
                          f"{_def_null_param(__document.doc_id)}, " \
                          f"{_text_param(_def_null_param(__document.title))}, " \
                          f"{_text_param(_def_null_param(__document.abstract))}, " \
                          f"{_text_param(_def_null_param(packed_text))}, " \
                          f"{_text_param(_def_null_param(__document.web_link))}, " \
                          f"{_text_param(_def_null_param(__document.local_link))}, " \
                          f"{_text_param(_def_null_param(other_data))}, " \
                          f"{_def_null_param(_datetime_param(__document.pub_date))}, " \
                          f"{_def_null_param(_datetime_param(__document.load_date))});"

            result = await conn.execute(text(query_param))
            await conn.commit()

        return result.fetchall()


if __name__ == "__main__":
    aas = Document.all_by_source_name('pci')
    print(aas)
