from src.sources_parser_platform.bus import Bus
from src.sources_parser_platform.module.spp_module import SPP_module
from src.sources_parser_platform.types import SPP_document


class FilterOnlyNewDocumentWithDB(SPP_module):
    """
    Модуль для фильтрации документов по их новизне, вызывая все документы из базы данных.

    DRAFT: Это тестовый модуль. Предполагается, что модули не могут напрямую обращаться к драйверам.
    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        new_doc = FilterOnlyNewDocumentWithDB.__filter(self.__previous_documents(), bus.documents.data)
        self.bus.documents = new_doc
        # Если есть новые документы, то их нужно сохранить
        if len(new_doc) > 0:
            self.__save_new_docs()

    def __previous_documents(self) -> list[SPP_document]:
        """
        Запрашивает у базы данных все документы по источнику
        :return:
        :rtype:
        """
        documents: list[SPP_document] = self.bus.database.doc.all_by_source_name(self.bus.source.data.name)
        return documents

    @staticmethod
    def __filter(_previous_documents: list[SPP_document], _new_documents: list[SPP_document]) \
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
        filtered: list[SPP_document] = []
        for cd in _new_documents:
            if FilterOnlyNewDocumentWithDB._is_new(cd, _previous_documents):
                filtered.append(cd)
        return filtered

    @staticmethod
    def _is_new(doc, _previous_documents):
        for pr_d in _previous_documents:
            if doc.hash == pr_d.hash:
                return False
        return True

    def __save_new_docs(self):

        for new_doc in self.bus.documents.data:
            self.bus.database.doc.safe_init(self.bus.source.data, new_doc)
        ...
