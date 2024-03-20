from src.spp.types import SPP_document
from src.spp.task.bus import Bus
from src.spp.task.module.base_module import BaseModule
# from src.spp.types import SPP_document, SppRefer
from src.spp.brokers.database import Document


class LastDocumentBySrc(BaseModule):
    """
    Модуль отдает последний документ источника

    Это нужно для того, чтобы парсер остановил работу, если наткнется на документ, который уже сканировал
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, {'dateonly': False})

    def __call__(self, *args, **kwargs):
        try:
            doc = Document.last(self.bus.source.data)
            if self.config.get('dateonly'):
                self.logger.debug('Document published was replace to data only')
                doc.pub_date = doc.pub_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
            return doc
        except ValueError:
            # Нет документа
            # raise ValueError(f'Document not found for source: {bus.source.data.name}') from e
            self.logger.debug(f'Document not found for source: {self.bus.source.data.name}')
            return None
