import re

from spp.task.bus import Bus
from spp.task.module.spp_module import SPP_module


class CutJunkCharactersFromDocumentText(SPP_module):
    """
    Модуль для защиты поля datetime
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, 'CutJunkCharactersFromDocumentText')

        PATTERN = r'[^a-zA-Z0-9;,. _]+'

        for doc in self.bus.documents.data:
            if isinstance(doc.text, str):
                doc.text = self.cut_junk_characters(doc.text, PATTERN)

    @staticmethod
    def cut_junk_characters(text: str, pattern) -> str:
        """
        Метод удаляет
        """
        return re.sub(pattern, ' ', text)
