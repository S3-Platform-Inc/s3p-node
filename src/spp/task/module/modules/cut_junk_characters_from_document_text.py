import re

from src.spp.task.bus import Bus
from src.spp.task.module.base_module import BaseModule


class CutJunkCharactersFromDocumentText(BaseModule):
    """
    Модуль для защиты поля datetime

    Пока мы обрезаем все, не входит в список: [a-zA-Z0-9;,. _]
    Это нужно, что запросы не ломались
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, {
            'PATTERN': r'[^a-zA-Z0-9;,. _]+',
            'REPL': ' ',
            'fields': ('text',)
        })
        count: int = 0
        for doc in self.bus.documents.data:
            is_cut: bool = False
            for field in self.config.get('fields'):
                # Не нравится такой
                value = doc.__getattribute__(field)
                if isinstance(value, str):
                    is_cut = True
                    cut_value = self.cut_junk_characters(value)
                    doc.__setattr__(field, cut_value)
                    self.logger.debug(f'{field} field of doc: {doc.title} was cut')
            if is_cut:
                count += 1

        self.logger.info(f'Count of cut docs: {count}')

    def cut_junk_characters(self, text: str) -> str:
        """
        Метод удаляет
        """
        return re.sub(self.config.get('PATTERN'), self.config.get('REPL'), text)
