from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from s3p_sdk.types import S3PDocument


class DeterminingFileMimetype(BaseModule):
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
        super().__init__(bus)

        for doc in self.bus.documents.data:
            self._determine(doc)

    def _determine(self, doc: S3PDocument):
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

    def _determine_by_document(self, doc: S3PDocument):
        """
        Определение типа файла по объекту документа
        :param doc:
        :type doc:
        :return:
        :rtype:
        """

        ...
