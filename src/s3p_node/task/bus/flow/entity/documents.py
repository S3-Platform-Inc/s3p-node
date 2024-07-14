"""
Поток № (2) шины

Объект сущности потока шины SPP, хранящий список документов (SPP_document)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..flow import Flow

if TYPE_CHECKING:
    from s3p_sdk.types import S3PDocument


class SppFeDocuments(Flow):
    data: list[S3PDocument]

    def __init__(self, documents: list[S3PDocument]):
        super().__init__()
        self.data = documents
        ...

    def update(self, document, new_document):
        """
        Обновляет данные документа
        :param document:
        :_type document:
        :param new_document:
        :_type new_document:
        """
        self.data[self.data.index(document)] = new_document
