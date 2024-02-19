from os import environ
import re
import logging

from .abc_plugin import AbcPlugin
from .config import Config, ParseConfig
from ..types import SppPlugin


class Plugin(AbcPlugin):

    def __init__(self, metadata: SppPlugin):
        self._log = logging.Logger(self.__class__.__name__)  # инициализация логов
        self.metadata = metadata
        self._config = ParseConfig(metadata.config).config()  # Датакласс конфигурации плагина

        # Абсолютный путь до архива плагинов
        self.BASE_PLUGIN_ARCHIVE_DIR_PATH = environ.get('SPP_ABSOLUTE_PATH_TO_PLUGIN_ARCHIVE')
        # Имя каталога плагина. Нужен для проверки на уже существующее имя.
        self.PLUGIN_CATALOG_NAME = re.sub(r"^(.+)\/", "", self.metadata.repository, 0, re.MULTILINE)

    @property
    def config(self) -> Config:
        """
        Returns the configuration of the plugin
        :return:
        """
        return self._config

    def __del__(self):
        pass


