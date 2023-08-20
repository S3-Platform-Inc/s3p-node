import logging
import os
from abc import ABCMeta

from src.types import ABC_task_parser, SPP_task_configuration


class ABC_Plugin(metaclass=ABCMeta):
    """
    Класс, представляющий плагин.
    """
    __src: str
    __parser: ABC_task_parser
    __config: SPP_task_configuration
    __logger: logging.Logger
    __type: str

    def __init__(self):
        ...

    ...
