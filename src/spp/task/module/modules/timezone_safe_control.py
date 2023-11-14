import datetime

from spp.task.bus import Bus
from spp.task.module.spp_module import SPP_module
from spp.types import SPP_document


class TimezoneSafeControl(SPP_module):
    """
    Модуль для защиты поля datetime
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, 'TimezoneSafeControl')

        for doc in self.bus.documents.data:
            if not self.__exists_timezone(doc):
                self._add_default_timezone(doc)

    @staticmethod
    def __exists_timezone(document: SPP_document) -> bool:
        # timezone is exits
        return not (document.pub_date.tzinfo is None or document.pub_date.tzinfo.utcoffset(document.pub_date) is None)

    @staticmethod
    def _add_default_timezone(document: SPP_document):
        # добавить логирование
        document.pub_date = document.pub_date.replace(tzinfo=datetime.timezone.utc)
