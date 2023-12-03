from __future__ import annotations

import os
from typing import Callable, TYPE_CHECKING
import multiprocessing

from spp.task.bus import Bus
from spp.task.bus.flow.entity import \
    SPP_FE_source, \
    SPP_FE_database, \
    SPP_FE_documents, \
    SPP_FE_options, \
    SPP_FE_fileserver, \
    SPP_FE_local_storage
from spp.task.module import get_module_by_name
from spp.task.task import Task
from spp.task.status import PREPARING, READY, WORKING, SUSPENDED, FINISHED, BROKEN

if TYPE_CHECKING:
    from spp.plugin.gitplugin import GitPlugin


class SPP_Pipeline_Task(Task):
    """
    Главный класс Задачи (Task). Содержит в себе только постобработку (Шины).

    :_modules: Содержит список подготовленных модулей.
    """

    _modules: multiprocessing.Queue[Callable]
    _current_module: Callable
    _current_module_name: str
    _bus: Bus

    def __init__(self, plugin: GitPlugin):
        super().__init__(plugin)

        self.upload_status(PREPARING)
        self._prepare()
        self.upload_status(READY)
        ...

    def run(self):
        self._log.debug(f"Task for {self._plugin.metadata.repository} plugin is running")
        self.upload_status(WORKING)
        self._cycle()
        self.upload_status(FINISHED)
        self._log.debug(f"Task for {self._plugin.metadata.repository} plugin is finished")

    def pause(self):
        self.upload_status(SUSPENDED)
        pass

    def stop(self):
        self.upload_status(FINISHED)
        pass

    def _cycle(self):
        self._log.debug(f"Main cycle of middleware is running")
        while not self._modules.empty():
            if self._status != WORKING:
                self._log.debug(f"Main cycle stopped or suspended")
                break

            self._current_module = self._modules.get()

            # initial and start current module
            try:
                self._log.debug(f"Module {self._current_module.__class__.__name__} start")
                self._current_module(self._bus)
                self._log.debug(f"Module {self._current_module.__class__.__name__} finished")
            except Exception as e:
                # Ошибка работы модуля. Если модуль является критическим, то вся обработка останавливается. Иначе продолжается
                if self._plugin.config.middleware.module_by_name(self._current_module.__class__.__name__).critical:
                    self._status = BROKEN
                    self._log.critical(
                        f"Module {self._current_module.__class__.__name__} is broken. Cycle was stopped")
                    raise NotImplemented(e)
                else:
                    self._log.error(
                        f"Module {self._current_module.__class__.__name__} is broken. Cycle continues")
                    continue
        else:
            self._log.debug(f"Main cycle of middleware is finished")

    def _prepare(self):
        self._log.debug("Task prepare start")
        self._setup_bus()
        self._module_preparing()
        self._log.debug("Task prepare completed")

    def _module_preparing(self):
        self._log.debug("Module preparing start")
        self._modules = multiprocessing.Queue()
        for module in self._plugin.config.middleware.modules:
            self._log.debug(f"Module '{module.name}' prepared")
            self._modules.put(get_module_by_name(module.name))
        self._log.debug("Module preparing completed")

    def _setup_bus(self):
        self._log.debug("Bus initializing")
        self._bus = Bus(
            self.__prepare_fe_options(),
            self.__prepare_fe_documents(),
            self.__prepare_fe_source(),
            self.__prepare_fe_database(),
            self.__prepare_fe_fileserver(),
            self.__prepare_fe_local_storage()
        )
        self._log.debug("Bus initialize completed")

    def __prepare_fe_options(self) -> SPP_FE_options:
        # Подготовка потока настроек для шины
        self._log.debug("Bus flow 'options' initializing")
        options = SPP_FE_options(self._plugin.config.middleware.modules)
        self._log.debug("Bus flow 'options' initialized")
        return options

    def __prepare_fe_documents(self) -> SPP_FE_documents:
        self._log.debug("Bus flow 'documents' initializing")
        self._log.debug("Bus flow 'documents' initialized")
        return SPP_FE_documents([])

    def __prepare_fe_source(self) -> SPP_FE_source:
        # подготовка потока источника для шины

        self._log.debug("Bus flow 'source' initializing")
        source_entity = SPP_FE_source(self._source)
        self._log.debug("Bus flow 'source' initialized")
        return source_entity

    def __prepare_fe_database(self) -> SPP_FE_database:
        # Подготовка потока базы данных для шины
        self._log.debug("Bus flow 'database' initializing")
        self._log.debug("Bus flow 'database' initialized")
        return SPP_FE_database()

    def __prepare_fe_fileserver(self) -> SPP_FE_fileserver:
        self._log.debug("Bus flow 'fileserver' initializing")
        fileserver = SPP_FE_fileserver(self._source)
        self._log.debug("Bus flow 'fileserver' initialized")
        return fileserver

    def __prepare_fe_local_storage(self) -> SPP_FE_local_storage:
        self._log.debug("Bus flow 'local storage' initializing")
        localstorage = SPP_FE_local_storage(self._source, os.environ.get('SPP_ABSOLUTE_PATH_TO_LOCAL_STORAGE'))
        self._log.debug("Bus flow 'local storage' initialized")
        return localstorage
