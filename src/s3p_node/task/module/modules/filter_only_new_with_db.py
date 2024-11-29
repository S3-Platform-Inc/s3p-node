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

        new_doc = self.__filter(bus.documents.data)
        self.bus.documents.data = new_doc
        self.logger.info(f"New {len(new_doc)} documents filtered")

    def __filter(self, _new_documents: list[S3PDocument]) -> list[S3PDocument]:
        """
        Метод фильтрует документы по их новизне
        :param _new_documents: Документы источника текущей итерации задачи
        :_type _new_documents:
        :return:
        :rtype:
        """
        self.logger.debug("filter process start")
        filtered: list[S3PDocument] = []
        for doc in _new_documents:
            if self._is_new(doc):
                filtered.append(doc)
        self.logger.debug("filter process finished")
        return filtered

    def _is_new(self, doc: S3PDocument):

        is_exist = self.bus.database.doc.exists(self.bus.source.data, doc)
        if is_exist:
            self.logger.debug(f"document named '{doc.title}' published '{doc.published}' already processed")
        else:
            self.logger.info(f"Found new document named '{doc.title}' published '{doc.published}'")
        return not is_exist
