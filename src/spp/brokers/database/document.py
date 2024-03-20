import json

from src.spp.types import SPP_document, SppRefer
from .main import ps_connection


class Document:
    schema: str = 'documents'

    @classmethod
    def littles(cls, source: SppRefer) -> list[SPP_document]:
        """
        Безопасное получение всех документов (title, web_link, pub_date), относящихся к одному источнику
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Document.schema}.littles', (source.id,))
                output = cursor.fetchall()
                res: list[SPP_document] = []
                for row in output:
                    res.append(SPP_document(
                        id=row[0],
                        title=row[2],
                        abstract=None,
                        text=None,
                        web_link=row[3],
                        local_link=None,
                        other_data=None,
                        pub_date=row[4],
                        load_date=None,
                    ))
                return res

    @classmethod
    def last(cls, source: SppRefer) -> SPP_document | ValueError:
        """
        Запрос последнего документа (title, web_link, pub_date) источника
        :param source:
        :return:
        """
        assert source.id or source.name
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                if source.id:
                    cursor.callproc(f'{Document.schema}.last', (source.id,))
                else:
                    cursor.callproc(f'{Document.schema}.last', (source.name,))
                output = cursor.fetchone()
                print(output)
                if not output:
                    raise ValueError(f'No document found for {source.id}')

                return SPP_document(
                        id=output[0],
                        title=output[2],
                        abstract=None,
                        text=None,
                        web_link=output[3],
                        local_link=None,
                        other_data=None,
                        pub_date=output[4],
                        load_date=None,
                    )


    @classmethod
    def save(cls, source: SppRefer, document: SPP_document) -> SPP_document:
        """

        save(
            sourceid integer,
            newtitle text,
            newabstract text,
            newtext text,
            newweblink text,
            newlocallink text,
            newotherdata json,
            newpubdate timestamp with time zone,
            newloaddate timestamp with time zone
        ) returns integer
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Document.schema}.save', (
                    int(source.id),
                    document.title,
                    document.abstract,
                    document.text,
                    document.web_link,
                    document.local_link,
                    json.dumps(document.other_data) if document.other_data else None,
                    document.pub_date,
                    document.load_date
                ))
                output = cursor.fetchone()  # Получим id документа
                document.id = output[0]
                return document


if __name__ == "__main__":
    ...
