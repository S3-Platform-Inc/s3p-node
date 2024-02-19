from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SppModule
from src.spp.types import SPP_document


class SaveDocumentToDB(SppModule):
    """
    Модуль для сохранения документов в базе данных.

    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        for doc in self.bus.documents.data:
            new_doc = self._save(doc)
            doc.id = new_doc.id
        self.logger.info(f'Updated {len(self.bus.documents.data)} documents')

    def _save(self, doc: SPP_document) -> SPP_document:
        new_doc = self.bus.database.doc.save(self.bus.source.data, doc)
        self.logger.debug(f'Save document title:{doc.title}, weblink: {doc.web_link}, pubdate:{doc.pub_date} to database')
        return new_doc
