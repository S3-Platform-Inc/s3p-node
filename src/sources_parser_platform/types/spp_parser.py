from abc import ABCMeta, abstractmethod

from .spp_document import SPP_document


class A_SPP_parser(metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def content(cls, category_type: str, subcategory_type: str) -> list[SPP_document]: ...

    @classmethod
    @abstractmethod
    def _parse(cls): ...
