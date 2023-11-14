import logging
import os

from .abc_plugin import ABC_Plugin
from ...exceptions.plugin import PluginNotFoundError


class LOCAL_Plugin(ABC_Plugin):

    __type = 'local'

    def __init__(self, path: str):
        super().__init__()
        self.__src = path
        self.logger = logging.Logger(self.__class__.__name__)
        self.__SPPFILERX = os.environ.get('SPP_PLUGIN_CONFIG_FILENAME')

        if self._is_sppfile() and self._is_valid_sppfile():
            config = self._sppfile()

            ...
        else:
            # Тут должна быть ошибка
            raise PluginNotFoundError(self.__src, self.__SPPFILERX, self.__logger)

        ...

    def _is_sppfile(self) -> bool:
        files: list = os.listdir(self.__src)
        return os.environ.get("SPP_PLUGIN_CONFIG_FILENAME") in files

    def _is_valid_sppfile(self) -> bool:
        # Тут затычка
        return True

    def _sppfile(self) -> list[str]:
        with open(self.__src + "\\" + self.__SPPFILERX, encoding='utf-8') as sppfile:
            self.logger.debug("SPPfile of plugin loadding")
            sppfile_lines = sppfile.readlines()
            self.logger.debug("SPPfile of plugin load completed")

            return sppfile_lines
    ...
