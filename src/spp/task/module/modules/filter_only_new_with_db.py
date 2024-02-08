from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SPP_module
from src.spp.types import SPP_document


class FilterOnlyNewDocumentWithDB(SPP_module):
    """
    Модуль для фильтрации документов по их новизне, вызывая все документы из базы данных.

    DRAFT: Это тестовый модуль. Предполагается, что модули не могут напрямую обращаться к драйверам.
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, 'FilterOnlyNewDocumentWithDB')

        new_doc = self.__filter(self.__previous_documents(), bus.documents.data)
        self.bus.documents.data = new_doc
        # Если есть новые документы, то их нужно сохранить
        if len(new_doc) > 0:
            self.__save_new_docs()
        self.logger.info(f"New {len(new_doc)} documents filtered")

    def __previous_documents(self) -> list[SPP_document]:
        """
        Запрашивает у базы данных все документы по источнику
        :return:
        :rtype:
        """
        self.logger.info(f"Receive previous documents by source '{self.bus.source.data.name}'")
        documents: list[SPP_document] = self.bus.database.doc.all_hashed_by_source_name(self.bus.source.data.name)
        self.logger.info(f"Received previous documents - {len(documents)}")
        return documents

    def __filter(self, _previous_documents: list[SPP_document], _new_documents: list[SPP_document]) \
            -> list[SPP_document]:
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
        filtered: list[SPP_document] = []
        for cd in _new_documents:
            if self._is_new(cd, _previous_documents):
                filtered.append(cd)
        self.logger.debug("filter process finished")
        return filtered

    def _is_new(self, doc: SPP_document, _previous_documents: list[SPP_document]):
        for pr_d in _previous_documents:
            if doc.hash == pr_d.hash:
                self.logger.debug(f"document named '{doc.title}' published '{doc.pub_date}' already processed")
                return False
        self.logger.info(f"Found new document named '{doc.title}' published '{doc.pub_date}'")
        return True

    def __save_new_docs(self):

        for new_doc in self.bus.documents.data:
            self.bus.database.doc.safe_init(self.bus.source.data, new_doc)
            self.logger.debug(f'Saved new document {new_doc.title} to database')
        ...
