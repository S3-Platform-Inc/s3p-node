import importlib.util
import os
import sys

from src.sources_parser_platform.modules import get_module_by_name
from src.sources_parser_platform.spp_language.parser import SPPL_parse

SPPFILERX = "SPPfile"


class Spp_plugin:
    _metadata: SPPL_parse
    _parser_class = None

    def __init__(self, source):
        self.__source = source
        self.__load_plugin()
        self._set_env()
        self._start()
        ...

    def __load_plugin(self):
        # Проверяем, что в указанной дерикториии есть файл SPPfile
        files: list = os.listdir(self.__source)
        if SPPFILERX in files:
            with open(self.__source + "\\" + SPPFILERX) as sppfile:
                self._metadata = SPPL_parse(sppfile.readlines())

        # Если находим
        if self._metadata.parser_filename + '.py' in files:
            spec = importlib.util.spec_from_file_location("module.parsers." + self._metadata.parser_filename,
                                                          self.__source + "\\" + self._metadata.parser_filename + ".py")
            foo = importlib.util.module_from_spec(spec)
            sys.modules["module.parsers." + self._metadata.parser_filename] = foo
            spec.loader.exec_module(foo)

            plugin_parser = foo.__dict__.__getitem__(self._metadata.parser_classname)
            self._parser_class = plugin_parser
        else:
            # Нужно обработать отсутствие файла с парсером
            raise NotImplemented
        ...

    def _set_env(self):
        ...

    def _start(self):
        # Тут подгружаются модули, которые нужны для запуска парсера
        # Например
        #           В тестовом случае необходим WebDriver для работы Selenium

        init = {key: get_module_by_name(value)() for key, value in self._metadata.parser_init_keywords}

        # Затем запускается модуль
        p_r = self._parser_class(**init).__getattribute__(self._metadata.parser_method)
        p_r()
