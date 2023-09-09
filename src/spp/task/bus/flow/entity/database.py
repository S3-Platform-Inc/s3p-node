"""
Поток № (4) шины

Объект сущности потока шины SPPApp, хранящий брокер для работы с базой данных
"""
from spp.brokers.database import Document as DB_Document, Source as DB_Source
from .. import Flow


class SPP_FE_database(Flow):
    _document: DB_Document
    _source: DB_Source

    def __init__(self):
        super().__init__()

        self._document = DB_Document()
        self._source = DB_Source()
        ...

    @property
    def doc(self) -> DB_Document:
        """
        Возвращает брокер схемы документа в базе данных
        :return:
        :rtype: DB_Document
        """
        return self._document

    @property
    def source(self) -> DB_Source:
        """
        Возвращает брокер схемы источника в базе данных
        :return:
        :rtype: DB_Source
        """
        return self._source
