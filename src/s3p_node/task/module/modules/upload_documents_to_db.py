from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from s3p_sdk.types import S3PDocument


class UploadDocumentToDB(BaseModule):
    """
    Модуль для обновления данных о документе в базе данных или создание записи в базе данных.

    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        for doc in self.bus.documents.data:
            self._upload(doc)

        self.logger.info(f'Updated {len(self.bus.documents.data)} documents')

    def _upload(self, doc: S3PDocument):
        self.bus.database.doc.save(self.bus.source.data, doc)
        self.logger.info(f'Upload document title:{doc.title}, pubdate:{doc.published} to database')
