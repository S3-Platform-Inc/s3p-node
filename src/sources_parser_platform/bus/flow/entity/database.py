from src.sources_parser_platform.brokers.db_broker import Document as DB_Document, Source as DB_Source
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
        return self._document

    @property
    def source(self) -> DB_Source:
        return self._source
