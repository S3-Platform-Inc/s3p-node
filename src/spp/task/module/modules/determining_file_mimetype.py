from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SPP_module
from src.spp.types import SPP_document


class DeterminingFileMimetype(SPP_module):
    """
    Модуль для определения типа файла документа

    DRAFT вместо options используются константы
    """

    # DRAFT
    # methods:  document | file
    # :document - определение типа файла по полям объекта SPP_document
    # :file - определение типа файла по части файла bytes(2048)
    DETERMINE_METHOD: str = 'document'

    def __init__(self, bus: Bus):
        super().__init__(bus, 'DeterminingFileMimetype')

        for doc in self.bus.documents.data:
            self._determine(doc)

    def _determine(self, doc: SPP_document):
        """
        Определение типа файла
        """

        if self.DETERMINE_METHOD == 'document':
            ...
        elif self.DETERMINE_METHOD == 'file':
            ...
        else:
            # DRAFT: подумать
            ...
        ...

    def _determine_by_document(self, doc: SPP_document):
        """
        Определение типа файла по объекту документа
        :param doc:
        :type doc:
        :return:
        :rtype:
        """

        ...
