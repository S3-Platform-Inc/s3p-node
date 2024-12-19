from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from s3p_sdk.types import S3PDocument


class SaveOnlyNewDocuments(BaseModule):
    """
    Модуль для сохранения документов в базе данных.

    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        for doc in self.bus.documents.data:
            try:
                new_doc = self._save(doc)
                doc.id = new_doc.id
            except ValueError as e:
                self.logger.debug(f"document named '{doc.title}' published '{doc.published}' already processed")
        self.logger.info(f'Updated {len(self.bus.documents.data)} documents')

    def _save(self, doc: S3PDocument) -> S3PDocument:
        new_doc = self.bus.database.doc.save_only_new(self.bus.source.data, doc)
        if new_doc.id == doc.id:
            self.logger.info(f'Update document title:{doc.title}, weblink: {doc.link}, pubdate:{doc.published} to database')
        else:
            self.logger.info(f'Save document title:{doc.title}, weblink: {doc.link}, pubdate:{doc.published} to database')
        return new_doc
