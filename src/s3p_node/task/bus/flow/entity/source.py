"""
Поток № (3) шины

Объект сущности потока шины SPP, содержащий информацию об источнике
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .. import Flow

if TYPE_CHECKING:
    from s3p_sdk.types import S3PRefer


class SppFeSource(Flow):
    _data: S3PRefer

    def __init__(self, ref: S3PRefer):
        super().__init__()

        self._data = ref

    @property
    def data(self) -> S3PRefer:
        """
        Возвращает информацию об источнике
        :return: объект источника
        :rtype: SPP_source
        """
        return self._data
