from abc import ABCMeta
from typing import Iterable


class ABC_SPP_Instruction(metaclass=ABCMeta):
    """
    Объект представляет инструкцию для платформы/
    """

    __LABEL: str
    __parameters: Iterable

    def __parse(self, params: list | tuple): ...
