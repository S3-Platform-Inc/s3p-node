"""
Поток № (3) шины

Объект сущности потока шины SPP, содержащий информацию об источнике
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import Flow

if TYPE_CHECKING:
    from src.spp.types import SppRefer


class SppFeSource(Flow):
    _data: SppRefer

    def __init__(self, ref: SppRefer):
        super().__init__()

        self._data = ref

    @property
    def data(self) -> SppRefer:
        """
        Возвращает информацию об источнике
        :return: объект источника
        :rtype: SPP_source
        """
        return self._data
