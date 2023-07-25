import importlib.util
import os
import pickle
import sys
from typing import Callable
import logging

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
from src.sources_parser_platform.exceptions.plugin import PluginNotFoundError

# SPPFILERX = "SPPfile"
SPPFILERX = os.environ.get('SPP_PLUGIN_CONFIG_FILENAME')

# .ENV
PATH_TO_LOCAL_STORAGE = r"E:\NSPK_DI\projects\NSPK_DI_parser\localstorage"  # DRAFT. Убрать в ENV.


# PATH_TO_LOCAL_STORAGE = os.path.join(os.path.dirname(__file__), '..\\..\\..', os.environ.get('LS_BASE_TEMP_DIR'))


class Spp_plugin:
    _metadata: SPPL_parse
    _parser_class: A_SPP_parser | Callable = None
    _parser_output: list[SPP_document]
    _source: SPP_source
    _bus: Bus

    # аргументом в модули

    def __init__(self, plugin_path):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.info("Plugin started")

        self.__plugin_path = plugin_path
        self.__load_plugin()
        self.__task_prepare()
        self.__middleware_cycle()

        self.logger.info("Plugin finished")
        ...

    def __load_plugin(self):
        """
        Метод загружает объекты плагина: класс парсера и конфигурацию.
        :return:
        :rtype:
        """
        self.logger.info("Plugin loading")

        # Проверяем, что в указанной директории есть файл SPPfile2
        files: list = os.listdir(self.__plugin_path)
        if SPPFILERX in files:
            with open(self.__plugin_path + "\\" + SPPFILERX, encoding='utf-8') as sppfile:
                self.logger.debug("SPPfile of plugin loadding")

                self._metadata = SPPL_parse(sppfile.readlines())

                self.logger.debug("SPPfile of plugin load completed")

            # Проверяем, что в указанной директории есть файл парсера
            if self._metadata.parser_filename + '.py' in files:
                self.logger.debug("Parser of plugin loadding")

                spec = importlib.util.spec_from_file_location("SPP.plugins." + self._metadata.parser_filename,
                                                              self.__plugin_path + "\\" + self._metadata.parser_filename + ".py")
                foo = importlib.util.module_from_spec(spec)
                sys.modules["SPP.plugins." + self._metadata.parser_filename] = foo
                spec.loader.exec_module(foo)

                plugin_parser = foo.__dict__.__getitem__(self._metadata.parser_classname)
                self._parser_class = plugin_parser
                self.logger.debug("Parser of plugin load completed")

            else:
                raise PluginNotFoundError(self.__plugin_path, self._metadata.parser_filename + '.py', self.logger)
        else:
            raise PluginNotFoundError(self.__plugin_path, SPPFILERX, self.logger)

        self.logger.info("Plugin load completed")
        ...

    def __middleware_cycle(self):

        self.logger.debug("Middleware start")

        for middleware in self._metadata.pipelines:
            self.logger.debug(f"module '{middleware}' prepared")
            get_module_by_name(middleware[0])(self._bus)

        self.logger.debug("Middleware finish")
        ...

    def _setup_bus(self):
        # Инициализация шины

        self.logger.debug("Bus initializing")

        self._bus = Bus(
            self.__prepare_fe_options(),
            self.__prepare_fe_documents_after_parser(),
            self.__prepare_fe_source(),
            self.__prepare_fe_database(),
            self.__prepare_fe_fileserver(),
            self.__prepare_fe_local_storage(),
            **self.__prepare_other_entities(),
        )

        self.logger.debug("Bus initialize completed")

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

        self.logger.debug("Bus flow 'source' initializing")

        # Сохранение источника и скачивание данных о нем из DB
        self._source = Source.safe(self._metadata.source_name)

        self.logger.debug("Bus flow 'source' initialized")
        return SPP_FE_source(self._source)

    def __prepare_fe_documents_after_parser(self) -> SPP_FE_documents:
        # Подготовка потока документа для шины
        self.logger.debug("Bus flow 'documents' initialized")

        # Эта вставка нужна для удаления Timezone из полей Datetime
        documents: list[SPP_document] = []
        for doc in self._parser_output:
            if doc.pub_date:
                doc.pub_date = doc.pub_date.replace(tzinfo=None)
            if doc.load_date:
                doc.load_date = doc.load_date.replace(tzinfo=None)
            documents.append(doc)

        return SPP_FE_documents(documents)

        # return SPP_FE_documents(self.DRAFT__load_temp('texted_document'))

    def __prepare_fe_options(self) -> SPP_FE_options:
        # Подготовка потока настроек для шины
        self.logger.debug("Bus flow 'options' initialized")
        return SPP_FE_options(self._metadata.pipelines)

    def __prepare_fe_database(self) -> SPP_FE_database:
        # Подготовка потока базы данных для шины
        self.logger.debug("Bus flow 'database' initialized")
        return SPP_FE_database()

    def __prepare_fe_fileserver(self) -> SPP_FE_fileserver:
        self.logger.debug("Bus flow 'fileserver' initialized")
        return SPP_FE_fileserver(Source.safe(self._metadata.source_name))

    def __prepare_fe_local_storage(self) -> SPP_FE_local_storage:
        self.logger.debug("Bus flow 'local storage' initialized")
        return SPP_FE_local_storage(Source.safe(self._metadata.source_name), PATH_TO_LOCAL_STORAGE)

    def __prepare_other_entities(self) -> dict:
        self.logger.debug("Bus additional flows initializing")

        entities = {}
        for _key, _value in self._metadata.bus_entities:
            # ОСТОРОЖНО, ХАРД КОД. ОБЯЗАТЕЛЬНО ПЕРЕДЕЛАТЬ
            if _value[0].startswith('PARSER/PCI/'):
                method = _value[0].split('/')[-1:][0]
                self.logger.debug(f"Bus added new flow named {_key} with module {method}")
                entities[_key] = self._parser_class.__getattribute__(method)
        ...

        self.logger.debug("Bus additional flows initialized")

        return entities

    def __task_prepare(self):
        self.logger.debug("Task prepare start")

        self._init_parser()
        self._start_parser()  # запуск парсера

        # self.DRAFT__save_temp(os.path.abspath(self.__plugin_path) + "\\" + self._metadata.parser_filename,
        #                       self._parser_output)

        self._setup_bus()  # инициализация шины

        self.logger.debug("Task prepare finished")
