from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SPP_document


class ABC_Plugin_Parser(metaclass=ABCMeta):
    """
    Абстрактный класс парсера плагина, который будет использоваться задачей (class SPP_Parser_Task)
    """

    @classmethod
    @abstractmethod
    def content(cls, *args, **kwargs) -> list[SPP_document]: ...

    @classmethod
    @abstractmethod
    def _parse(cls, *args, **kwargs): ...
