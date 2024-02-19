import json

from . import ps_connection
from src.spp.types import SppNode


class Node:
    """
    Схема источника для взаимодействия с базой данных.
    """

    schema: str = 'nodes'

    @staticmethod
    def init(node: SppNode) -> SppNode:
        """
        Инициализация
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Node.schema}.init', (node.name, node.ip, json.dumps(node.config)))
                output = cursor.fetchone()
                node.id = int(output[0])
                return node

    @staticmethod
    def alive(node: SppNode) -> SppNode:
        """
        Метод, который говорит БД о том, что узел жив
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Node.schema}.alive', (node.id,))
                output = cursor.fetchone()
                node.session = int(output[0]) if output[0] else None
                return node


if __name__ == "__main__":
    ...
