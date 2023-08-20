from typing import Callable

from src.types.abc_task_parser import ABC_task_parser
from src.types import SPP_task_configuration


class SPP_task:
    """
    Главный класс Задачи (Task). На вход получает класс парсера и настройки задачи
    """

    _PARSER_CLASS: ABC_task_parser | Callable = None
    _config: SPP_task_configuration

    def __init__(self, parser_class: ABC_task_parser, config: SPP_task_configuration):
        self._PARSER_CLASS = parser_class
        self._config = config
        ...
