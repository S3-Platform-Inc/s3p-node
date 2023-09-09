"""
Поток № (3) шины

Объект сущности потока шины SPPApp, содержащий информацию об источнике
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import Flow

if TYPE_CHECKING:
    from spp.types import SPP_source


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
