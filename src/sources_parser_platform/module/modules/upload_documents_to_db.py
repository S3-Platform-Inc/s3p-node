from src.sources_parser_platform.bus import Bus
from src.sources_parser_platform.module.spp_module import SPP_module
from src.sources_parser_platform.types import SPP_document


class UploadDocumentToDB(SPP_module):
    """
    Модуль для фильтрации документов по их новизне, вызывая все документы из базы данных.

    DRAFT: Это тестовый модуль. Предполагается, что модули не могут напрямую обращаться к драйверам.
    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        for doc in self.bus.documents.data:
            self._upload(doc)

    def _upload(self, doc: SPP_document):
        res = self.bus.database.doc.safe_update(self.bus.source.data, doc)
        print(res)
        ...

    def _draft_upload(self, doc: SPP_document):
        """
        !! DRAFT

        Временный метод, который ограничивает размер передаваемого поля text в базу данных
        :param doc:
        :type doc:
        :return:
        :rtype:
        """
        max_length = 2 << 16 if len(doc.text) > (2 << 16) else len(doc.text)
        doc.text = doc.text[:max_length]
        res = self.bus.database.doc.safe_update(self.bus.source.data, doc)
        print(res)
