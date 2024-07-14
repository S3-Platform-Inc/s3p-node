from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from s3p_sdk.types import S3PDocument


class FilterOnlyNewDocumentWithDB(BaseModule):
    """
    Модуль для фильтрации документов по их новизне, вызывая все документы из базы данных.

    DRAFT: Это тестовый модуль. Предполагается, что модули не могут напрямую обращаться к драйверам.
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, {'save': False})

        new_doc = self.__filter(self.__previous_documents(), bus.documents.data)
        self.bus.documents.data = new_doc
        self.logger.info(f"New {len(new_doc)} documents filtered")
        # Если есть новые документы, то их можно сохранить
        if self.config.get('save') and len(new_doc) > 0:
            self.__save_new_docs()
            self.logger.get(f"Saved {len(new_doc)} documents to DB")

    def __previous_documents(self) -> list[S3PDocument]:
        """
        Запрашивает у базы данных все документы по источнику
        :return:
        :rtype:
        """
        self.logger.info(f"Receive previous documents by source '{self.bus.source.data.name}'")
        documents: list[S3PDocument] = self.bus.database.doc.littles(self.bus.source.data)
        self.logger.info(f"Received previous documents - {len(documents)}")
        return documents

    def __filter(self, _previous_documents: list[S3PDocument], _new_documents: list[S3PDocument]) \
            -> list[S3PDocument]:
        """
        Метод фильтрует документы по их новизне
        :param _previous_documents: Все документы по источнику
        :_type _previous_documents:
        :param _new_documents: Документы источника текущей итерации задачи
        :_type _new_documents:
        :return:
        :rtype:
        """
        self.logger.debug("filter process start")
        filtered: list[S3PDocument] = []
        for cd in _new_documents:
            if self._is_new(cd, _previous_documents):
                filtered.append(cd)
        self.logger.debug("filter process finished")
        return filtered

    def _is_new(self, doc: S3PDocument, _previous_documents: list[S3PDocument]):
        for pr_d in _previous_documents:
            if doc.hash == pr_d.hash:
                self.logger.debug(f"document named '{doc.title}' published '{doc.published}' already processed")
                return False
        self.logger.info(f"Found new document named '{doc.title}' published '{doc.published}'")
        return True

    def __save_new_docs(self):

        for new_doc in self.bus.documents.data:
            self.bus.database.doc.save(self.bus.source.data, new_doc)
            self.logger.info(f'Saved new document {new_doc.title} to database')
        ...
