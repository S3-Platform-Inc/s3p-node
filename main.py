"""
DRAFT

Главный файл

Запускает задачу для одного плагина.

:plugin_path: Путь до каталога с файлами плагина ( <файл парсера источника>.py ; SPPfile )
"""
import logging
import os
from logging import config

from dotenv import load_dotenv

config.fileConfig("scripts/logger/dev_logger.conf")
load_dotenv('.env')

from src.task.plugin.plugin import Spp_plugin

SOURCE = 'pci'

log = logging.getLogger(__name__)
plugin_path = rf'{os.getenv("SPP_PATH_TO_PLUGIN")}\NSPK-DI-SPP-plugin-{SOURCE}'


try:
    Spp_plugin(plugin_path)
except Exception as e:
    print(e)
