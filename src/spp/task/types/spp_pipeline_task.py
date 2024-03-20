from __future__ import annotations

import multiprocessing
import os
from typing import Callable, TYPE_CHECKING

from src.spp.task.bus import Bus
from src.spp.task.bus.flow.entity import \
    SppFeSource, \
    SppFeDatabase, \
    SppFeDocuments, \
    SppFeOptions, \
    SppFeFileserver, \
    SppFeLocalStorage
from src.spp.task.module import get_module_by_name
from src.spp.task.status import WORKING, BROKEN
from src.spp.task.task import Task

if TYPE_CHECKING:
    from src.spp.plugin.abc_plugin import AbcPlugin
    from src.spp.types import SppTask
    from src.spp.plugin.config.schemes import Module


class SppPipelineTask(Task):
    """
    Главный класс Задачи (Task). Содержит в себе только постобработку (Шины).

    :_modules: Содержит список подготовленных модулей.
    """

    _modules: multiprocessing.Queue[Callable]
    _current_module: Callable
    _bus: Bus

    def __init__(self, task: SppTask, plugin: AbcPlugin):
        super().__init__(task, plugin)

        self._prepare()

    def run(self):
        self._log.debug(f"Task ID:{self._task.id} SesID: {self._task.session_id} "
                        f"for plugin:{self._plugin.metadata.repository} is running")
        self.upload_status(WORKING)
        self._cycle()
        self._log.debug(f"Task ID:{self._task.id} SesID: {self._task.session_id} "
                        f"for plugin:{self._plugin.metadata.repository} is finished")

    def pause(self): ...

    def stop(self): ...

    def _cycle(self):
        self._log.debug(f"Main cycle of middleware is running")
        while not self._modules.empty():
            if self._status != WORKING:
                self._log.debug(f"Main cycle stopped or suspended")
                break

            self._current_module = self._modules.get()

            # initial and start current module
            try:
                self._log.debug(f"Module {self._current_module.__name__} start")
                self._current_module(self._bus)
                self._log.debug(f"Module {self._current_module.__name__} finished")
            except Exception as _e:
                # Ошибка работы модуля. Если модуль является критическим, то вся обработка останавливается.
                # Иначе продолжается
                if self._plugin.config.middleware.module_by_name(self._current_module.__name__).critical:
                    self._status = BROKEN
                    self._log.critical(
                        f"Module {self._current_module.__name__} is broken. Cycle was stopped. Error message: {_e}")
                    raise _e
                else:
                    self._log.error(
                        f"Module {self._current_module.__name__} is broken. Cycle continues. Error message: {_e}")
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

    def __prepare_fe_options(self) -> SppFeOptions:
        # Подготовка потока настроек для шины
        self._log.debug("Bus flow 'options' initializing")
        # Вот тут мы находим все модули в конфигурации и выгружаем их параметры
        # модули из middleware и entryObject
        entry_modules = []
        for param in self._plugin.config.payload.entry_params:
            if isinstance((module := param.value), Module) and module.options:
                entry_modules.append(module)

        for module in self._plugin.config.middleware.modules:
            if module.options:
                entry_modules.append(module)

        options = SppFeOptions(tuple(entry_modules))
        self._log.debug("Bus flow 'options' initialized")
        return options

    def __prepare_fe_documents(self) -> SppFeDocuments:
        self._log.debug("Bus flow 'documents' initializing")
        self._log.debug("Bus flow 'documents' initialized")
        return SppFeDocuments([])

    def __prepare_fe_source(self) -> SppFeSource:
        # подготовка потока источника для шины

        self._log.debug("Bus flow 'source' initializing")
        source_entity = SppFeSource(self._task.refer)
        self._log.debug("Bus flow 'source' initialized")
        return source_entity

    def __prepare_fe_database(self) -> SppFeDatabase:
        # Подготовка потока базы данных для шины
        self._log.debug("Bus flow 'database' initializing")
        self._log.debug("Bus flow 'database' initialized")
        return SppFeDatabase()

    def __prepare_fe_fileserver(self) -> SppFeFileserver:
        self._log.debug("Bus flow 'fileserver' initializing")
        fileserver = SppFeFileserver(self._task.refer)
        self._log.debug("Bus flow 'fileserver' initialized")
        return fileserver

    def __prepare_fe_local_storage(self) -> SppFeLocalStorage:
        self._log.debug("Bus flow 'local storage' initializing")
        localstorage = SppFeLocalStorage(self._task.refer, os.environ.get('SPP_ABSOLUTE_PATH_TO_LOCAL_STORAGE'))
        self._log.debug("Bus flow 'local storage' initialized")
        return localstorage
