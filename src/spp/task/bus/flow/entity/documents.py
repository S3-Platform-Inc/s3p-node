"""
Поток № (2) шины

Объект сущности потока шины SPP, хранящий список документов (SPP_document)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..flow import Flow

if TYPE_CHECKING:
    from spp.types import SPP_document


class SPP_FE_documents(Flow):
    data: list[SPP_document]

    def __init__(self, documents: list[SPP_document]):
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
