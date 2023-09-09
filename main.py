"""
DRAFT

Главный файл

Запускает задачу для одного плагина.

:plugin_path: Путь до каталога с файлами плагина ( <файл парсера источника>.py ; SPPfile )
"""
import logging
from logging import config

from dotenv import load_dotenv

config.fileConfig("configurations/logger/dev_logger.conf")
load_dotenv('.env')

# from spp.task import Spp_plugin
from src.spp import SPPApp

# SOURCE = 'pci'

log = logging.getLogger(__name__)
# plugin_path = rf'{os.getenv("SPP_PATH_TO_PLUGIN")}\NSPK-DI-SPPApp-spp_plugin-{SOURCE}'

if __name__ == "__main__":
    spp = SPPApp()
    spp.run()
