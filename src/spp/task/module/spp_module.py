import logging

from src.spp.task.bus import Bus


class SppModule:
    """
    Базовый класс Модуль
    """

    def __init__(self, bus: Bus):
        self.bus: Bus = bus
        self.logger = logging.getLogger(self.__class__.__name__)
