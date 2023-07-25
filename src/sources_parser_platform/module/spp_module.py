import logging

from src.sources_parser_platform.bus import Bus


class SPP_module:
    """
    Базовый класс Модуль
    """

    def __init__(self, bus: Bus, classname: str = None):
        self.bus: Bus = bus
        self.logger = logging.getLogger(self.__class__.__name__)

        if classname:
            start_message = f"module '{classname}' start"
        else:
            start_message = f"module start"
        self.logger.info(start_message)
