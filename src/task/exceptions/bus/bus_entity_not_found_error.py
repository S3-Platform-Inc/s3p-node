"""

"""
from logging import Logger


class BusEntityNotFoundError(KeyError):
    """
    Ошибка используется если не найдена сущность шины по уникальному ключу
    """

    def __init__(self, entity_key: str, logger: Logger = None):
        message = f"'{entity_key}' entity not found"
        super().__init__(message)

        if logger:
            logger.error(message)
        ...
