from src.spp.task.bus import Bus
from src.spp.task.module.base_module import BaseModule
from src.spp.types import SPP_document


class SaveDocumentToDB(BaseModule):
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
        if new_doc.id == doc.id:
            self.logger.debug(f'Update document title:{doc.title}, weblink: {doc.web_link}, pubdate:{doc.pub_date} to database')
        else:
            self.logger.debug(f'Save document title:{doc.title}, weblink: {doc.web_link}, pubdate:{doc.pub_date} to database')
        return new_doc
