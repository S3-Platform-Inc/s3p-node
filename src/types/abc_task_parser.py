from abc import ABCMeta, abstractmethod

from .spp_document import SPP_document


class ABC_task_parser(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def content(cls, category_type: str, subcategory_type: str) -> list[SPP_document]: ...

    @classmethod
    @abstractmethod
    def _parse(cls): ...
