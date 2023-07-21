import importlib.util
import os
import pickle
import sys
from typing import Callable

from src.sources_parser_platform.types import SPP_source, A_SPP_parser, SPP_document
from src.sources_parser_platform.brokers.db_broker import Source
from src.sources_parser_platform.bus import Bus
from src.sources_parser_platform.bus.flow.entity import \
    SPP_FE_source, \
    SPP_FE_database, \
    SPP_FE_documents, \
    SPP_FE_options, \
    SPP_FE_fileserver, \
    SPP_FE_local_storage
from src.sources_parser_platform.module import get_module_by_name
from src.sources_parser_platform.spp_language.parser import SPPL_parse

SPPFILERX = "SPPfile"
TEMP_FOLDER = ".temp_plugin"

# .ENV
PARSER_MAIN_CLASS_METHOD = "content"
PATH_TO_LOCAL_STORAGE = r"E:\NSPK_DI\projects\NSPK_DI_parser\localstorage"  # DRAFT. Убрать в ENV.


class Spp_plugin:
    _metadata: SPPL_parse
    _parser_class: A_SPP_parser | Callable = None
    _parser_output: list[SPP_document]
    _source: SPP_source
    _bus: Bus

    # аргументом в модули

    def __init__(self, plugin_path):
        self.__plugin_path = plugin_path
        self.__load_plugin()
        self.__task_prepare()
        self.__middleware_cycle()
        ...

    def __load_plugin(self):
        # Проверяем, что в указанной дерикториии есть файл SPPfile
        files: list = os.listdir(self.__plugin_path)
        if SPPFILERX in files:
            with open(self.__plugin_path + "\\" + SPPFILERX) as sppfile:
                self._metadata = SPPL_parse(sppfile.readlines())

        # Если находим
        if self._metadata.parser_filename + '.py' in files:
            spec = importlib.util.spec_from_file_location("SPP_module.parsers." + self._metadata.parser_filename,
                                                          self.__plugin_path + "\\" + self._metadata.parser_filename + ".py")
            foo = importlib.util.module_from_spec(spec)
            sys.modules["SPP_module.parsers." + self._metadata.parser_filename] = foo
            spec.loader.exec_module(foo)

            plugin_parser = foo.__dict__.__getitem__(self._metadata.parser_classname)
            self._parser_class = plugin_parser


        else:
            # Нужно обработать отсутствие файла с парсером
            raise NotImplemented

        # Создание контейнера для временных сохранений
        ...

    def __middleware_cycle(self):

        for middleware in self._metadata.pipelines:
            print(middleware)
            get_module_by_name(middleware[0])(self._bus)

        print(self._bus)
        # self.DRAFT__save_temp('texted_document', self._bus.documents.data)
        ...

    def _setup_bus(self):
        # Инициализация шины

        self._bus = Bus(
            self.__prepare_fe_options(),
            self.__prepare_fe_documents_after_parser(),
            self.__prepare_fe_source(),
            self.__prepare_fe_database(),
            self.__prepare_fe_fileserver(),
            self.__prepare_fe_local_storage(),
            **self.__prepare_other_entities(),
        )

        ...

    def _init_parser(self):
        # Тут подгружаются модули, которые нужны для запуска парсера
        # Например
        #           В тестовом случае необходим WebDriver для работы Selenium

        init = {key: get_module_by_name(value)() for key, value in
                self._metadata.parser_init_keywords}

        # Затем запускается модуль
        # DRAFT не подтягивается
        self._parser_class = self._parser_class(**init)

    def _start_parser(self):

        # Затем запускается модуль
        # DRAFT не подтягивается
        p_r = self._parser_class.__getattribute__(self._metadata.parser_method)

        output = p_r()
        # OR when DRAFT
        # output = []
        # OR when need return dump documents
        # output = self.DRAFT__load_temp(os.path.abspath(self.__plugin_path) + "\\" + self._metadata.parser_filename)[2:]

        self._parser_output = output

    def DRAFT__save_temp(self, filename, data):
        with open(filename + '.temp', mode='wb') as temp_cont:
            pickle.dump(data, temp_cont, protocol=pickle.HIGHEST_PROTOCOL)
        ...

    def DRAFT__load_temp(self, filename):
        with open(filename + '.temp', mode='rb') as temp_cont:
            return pickle.load(temp_cont)

    def __prepare_fe_source(self) -> SPP_FE_source:
        # подготовка потока источника для шины

        # Сохранение источника и скачивание данных о нем из DB
        self._source = Source.safe(self._metadata.source_name)
        return SPP_FE_source(self._source)

    def __prepare_fe_documents_after_parser(self) -> SPP_FE_documents:
        # Подготовка потока документа для шины
        return SPP_FE_documents(self._parser_output)

        # return SPP_FE_documents(self.DRAFT__load_temp('texted_document'))

    def __prepare_fe_options(self) -> SPP_FE_options:
        # Подготовка потока настроек для шины
        return SPP_FE_options(self._metadata.pipelines)

    def __prepare_fe_database(self) -> SPP_FE_database:
        # Подготовка потока базы данных для шины
        return SPP_FE_database()

    def __prepare_fe_fileserver(self) -> SPP_FE_fileserver:
        return SPP_FE_fileserver(Source.safe(self._metadata.source_name))

    def __prepare_fe_local_storage(self) -> SPP_FE_local_storage:
        return SPP_FE_local_storage(Source.safe(self._metadata.source_name), PATH_TO_LOCAL_STORAGE)

    def __prepare_other_entities(self) -> dict:
        entities = {}
        for _key, _value in self._metadata.bus_entities:
            # ОСТОРОЖНО, ХАРД КОД. ОБЯЗАТЕЛЬНО ПЕРЕДЕЛАТЬ
            if _value[0].startswith('PARSER/PCI/'):
                method = _value[0].split('/')[-1:][0]
                print(method)
                entities[_key] = self._parser_class.__getattribute__(method)
        ...

        return entities

    def __task_prepare(self):

        self._init_parser()
        self._start_parser()  # запуск парсера

        # self.DRAFT__save_temp(os.path.abspath(self.__plugin_path) + "\\" + self._metadata.parser_filename,
        #                       self._parser_output)

        self._setup_bus()  # инициализация шины
