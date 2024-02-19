import datetime

from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SppModule
from src.spp.types import SPP_document


class TimezoneSafeControl(SppModule):
    """
    Модуль для защиты поля datetime
    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        count: int = 0
        for doc in self.bus.documents.data:
            if not self.__exists_timezone(doc):
                count += 1
                self._add_default_timezone(doc)
                self.logger.debug(f'Added timezone to datetime in document {doc.title}')
        self.logger.info(f'{len(self.bus.documents.data)} documents which timezone has been added')

    @staticmethod
    def __exists_timezone(document: SPP_document) -> bool:
        # timezone is exits
        return not (document.pub_date.tzinfo is None or document.pub_date.tzinfo.utcoffset(document.pub_date) is None)

    @staticmethod
    def _add_default_timezone(document: SPP_document):
        # добавить логирование
        document.pub_date = document.pub_date.replace(tzinfo=datetime.timezone.utc)
