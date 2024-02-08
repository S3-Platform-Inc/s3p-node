from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SPP_module
from src.spp.types import SPP_document


class UploadDocumentToDB(SPP_module):
    """
    Модуль для обновления данных о документе в базе данных или создание записи в базе данных.

    """

    def __init__(self, bus: Bus):
        super().__init__(bus, 'UploadDocumentToDB')

        for doc in self.bus.documents.data:
            self._upload(doc)

        self.logger.info(f'Updated {len(self.bus.documents.data)} documents')

    def _upload(self, doc: SPP_document):
        self.bus.database.doc.safe_update(self.bus.source.data, doc)
        self.logger.debug(f'Upload document title:{doc.title}, pubdate:{doc.pub_date} to database')
