"""
DRAFT

Главный файл

Запускает задачу для одного плагина.

:plugin_path: Путь до каталога с файлами плагина ( <файл парсера источника>.py ; SPPfile2 )
"""
from logging import config

from src.sources_parser_platform.plugin.plugin import Spp_plugin

config.fileConfig("scripts/logger/dev_logger.conf")

plugin_path = r'< Path to plugin>'
pl = Spp_plugin(plugin_path)
