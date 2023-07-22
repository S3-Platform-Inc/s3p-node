import logging

from src.sources_parser_platform.bus import Bus


class SPP_module:
    """
    Базовый класс Модуль
    """

    def __init__(self, bus: Bus):
        self.bus: Bus = bus
        self.logger = logging.getLogger(self.__class__.__name__)
