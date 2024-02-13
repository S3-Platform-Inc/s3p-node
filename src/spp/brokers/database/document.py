import json

from src.spp.types import SPP_document, SPP_source
from .main import psConnection


class Document:

    @classmethod
    def little_documents(cls, source_name: str) -> list[SPP_document]:
        """
        Безопасное получение всех документов (title, web_link, pub_date), относящихся к одному источнику
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.get_all_documents_for_hash_by_source', (None, source_name, ))
                output = cursor.fetchall()
                res: list[SPP_document] = []
                for row in output:
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
    def init(cls, source: SPP_source, document: SPP_document) -> bool:
        """

        :param source:
        :type source:
        :param document:
        :type document:
        :return:
        :rtype:
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.safe_init_document', (
                    int(source.src_id),
                    source.name,
                    document.title,
                    document.abstract,
                    document.web_link,
                    document.pub_date
                ))
                output = cursor.fetchone()
                return output[0][0]

    @classmethod
    def update(cls, source: SPP_source, document: SPP_document) -> bool:
        """
        Безопасное обновление или добавление данных о документе.

        Если возвращается True - то данные обновились
        Если возвращается False - то документа не было в таблице. Он был добавлен в таблицу.
        :return:
        :rtype:
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.safe_update_document', (
                    source.src_id,
                    source.name,
                    document.doc_id,
                    document.title,
                    document.abstract,
                    document.text,
                    document.web_link,
                    document.local_link,
                    json.dumps(document.other_data),
                    document.pub_date,
                    document.load_date
                ))
                output = cursor.fetchone()
                return output[0][0]


if __name__ == "__main__":
    ...
