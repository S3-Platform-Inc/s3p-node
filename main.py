"""
DRAFT

Главный файл

Запускает задачу для одного плагина.

:plugin_path: Путь до каталога с файлами плагина ( <файл парсера источника>.py ; SPPfile )
"""
from sources_parser_platform.plugin.plugin import Spp_plugin

plugin_path = r'E:\NSPK_DI\projects\plugins\NSPK-DI-SPP-pci'
pl = Spp_plugin(plugin_path)
