from src.task.bus import Bus
from src.task.module.spp_module import SPP_module
from src.types import SPP_document


class UploadDocumentToDB(SPP_module):
    """
    Модуль для обновления данных о документе в базе данных или создание записи в базе данных.

    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        for doc in self.bus.documents.data:
            self._upload(doc)

    def _upload(self, doc: SPP_document):
        self.bus.database.doc.safe_update(self.bus.source.data, doc)

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
