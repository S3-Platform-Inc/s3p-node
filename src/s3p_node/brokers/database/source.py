from . import ps_connection
from s3p_sdk.types import S3PRefer


class Source:
    """
    Схема источника для взаимодействия с базой данных.
    """

    @staticmethod
    def safe(_name: str) -> S3PRefer:
        """
        Безопасное получение данные об источнике. В случае, если в базе данных нет записи об источнике, он добавится.
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.safe_get_source', (_name,))
                output = cursor.fetchone()
                return S3PRefer(*output)


if __name__ == "__main__":
    ...
