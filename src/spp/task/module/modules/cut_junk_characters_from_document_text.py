import re

from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SppModule


class CutJunkCharactersFromDocumentText(SppModule):
    """
    Модуль для защиты поля datetime

    Пока мы обрезаем все, не входит в список: [a-zA-Z0-9;,. _]
    Это нужно, что запросы не ломались
    """

    def __init__(self, bus: Bus):
        super().__init__(bus)

        self.PATTERN: str = r'[^a-zA-Z0-9;,. _]+'

        count: int = 0

        for doc in self.bus.documents.data:
            is_cut: bool = False
            if isinstance(doc.title, str):
                doc.title = self.cut_junk_characters(doc.title)
                is_cut = True
                self.logger.debug(f'title field of doc: {doc.title} was cut')
            if isinstance(doc.text, str):
                doc.text = self.cut_junk_characters(doc.text)
                is_cut = True
                self.logger.debug(f'text field of doc: {doc.title} was cut')
            if isinstance(doc.abstract, str):
                doc.abstract = self.cut_junk_characters(doc.abstract)
                is_cut = True
                self.logger.debug(f'abstract field of doc: {doc.title} was cut')
            if is_cut:
                count += 1

        self.logger.info(f'Count of cut docs: {count}')

    def cut_junk_characters(self, text: str) -> str:
        """
        Метод удаляет
        """
        return re.sub(self.PATTERN, ' ', text)
