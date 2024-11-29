import datetime

from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule


class TimezoneSafeControl(BaseModule):
    """
    Модуль для защиты поля datetime

    config (key: value)
        fields: (field name 1, field name 2, ...)
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, {
            'fields': ('published', 'loaded',)
        })

        for doc in self.bus.documents.data:
            # Принято решения делать хард проверку так как:
            #   - в документе всего 2 поля с датой
            #   - использовать _getattribute_ и _setattr_ не хочется.
            if 'published' in self.config.get('fields') and doc.published and not self.__exists_timezone(doc.published):
                doc.published = doc.published.replace(tzinfo=datetime.timezone.utc)
                self.logger.debug(f'Added timezone to pub_date in document {doc.id}, {doc.title}')
            if 'loaded' in self.config.get('fields') and doc.loaded and not self.__exists_timezone(doc.loaded):
                doc.loaded = doc.loaded.replace(tzinfo=datetime.timezone.utc)
                self.logger.debug(f'Added timezone to load_date in document {doc.id}, {doc.title}')
        self.logger.info(f'{len(self.bus.documents.data)} documents which timezone has been added')

    @staticmethod
    def __exists_timezone(date: datetime) -> bool:
        # timezone is exits
        return not (date.tzinfo is None or date.tzinfo.utcoffset(date) is None)
