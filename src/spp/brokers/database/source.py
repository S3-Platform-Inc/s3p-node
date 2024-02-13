from . import psConnection
from src.spp.types import SPP_source


class Source:
    """
    Схема источника для взаимодействия с базой данных.
    """

    @staticmethod
    def safe(_name: str) -> SPP_source:
        """
        Безопасное получение данные об источнике. В случае, если в базе данных нет записи об источнике, он добавится.
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.safe_get_source', (_name,))
                output = cursor.fetchone()
                return SPP_source(*output)


if __name__ == "__main__":
    aas = Source.safe('pci')
    print(aas, aas.name)
