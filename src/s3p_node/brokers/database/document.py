import json

from s3p_sdk.types import S3PDocument, S3PRefer
from .main import ps_connection


class Document:
    schema: str = 'documents'

    @classmethod
    def littles(cls, source: S3PRefer) -> list[S3PDocument]:
        """
        Безопасное получение всех документов (title, web_link, pub_date), относящихся к одному источнику
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Document.schema}.littles', (source.id,))
                output = cursor.fetchall()
                res: list[S3PDocument] = []
                for row in output:
                    res.append(S3PDocument(
                        id=row[0],
                        title=row[2],
                        abstract=None,
                        text=None,
                        link=row[3],
                        storage=None,
                        other=None,
                        published=row[4],
                        loaded=None,
                    ))
                return res

    @classmethod
    def last(cls, source: S3PRefer) -> S3PDocument | ValueError:
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

                return S3PDocument(
                        id=output[0],
                        title=output[2],
                        abstract=None,
                        text=None,
                        link=output[3],
                        storage=None,
                        other=None,
                        published=output[4],
                        loaded=None,
                    )


    @classmethod
    def save(cls, source: S3PRefer, document: S3PDocument) -> S3PDocument:
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
                    document.link,
                    document.storage,
                    json.dumps(document.other) if document.other else None,
                    document.published,
                    document.loaded
                ))
                output = cursor.fetchone()  # Получим id документа
                document.id = output[0]
                return document


if __name__ == "__main__":
    ...
