"""
Поток № (3) шины

Объект сущности потока шины SPP, содержащий информацию об источнике
"""
from src.sources_parser_platform.types.spp_source import SPP_source
from .. import Flow


class SPP_FE_source(Flow):
    _data: SPP_source

    def __init__(self, src: SPP_source):
        super().__init__()

        self._data = src

    @property
    def data(self) -> SPP_source:
        """
        Возвращает информацию об источнике
        :return: объект источника
        :rtype: SPP_source
        """
        return self._data
