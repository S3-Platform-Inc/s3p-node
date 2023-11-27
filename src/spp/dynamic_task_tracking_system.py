from __future__ import annotations

import multiprocessing
import time
from logging import getLogger
from typing import TYPE_CHECKING

from github import UnknownObjectException, RateLimitExceededException

from .plugin.git_plugin import GIT_Plugin
from .brokers.database import Plugin as db_plugin, Task as db_task
from .task.types.spp_parser_task import SPP_Parser_Task
from .task.status import FINISHED

if TYPE_CHECKING:
    from src.spp.types import SPP_plugin


class DynamicTaskTrackingSystem(multiprocessing.Process):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _plugins: multiprocessing.Queue
    _current_plugin: SPP_plugin | None

    def __init__(self):
        super().__init__()
        self._log = getLogger()
        self._plugins = multiprocessing.Queue()
        self._current_plugin = None

    def run(self):
        self._log.debug("Main tracking system is start")
        try:
            self._main_tracking_loop()
        except Exception as e:
            while not self._plugins.empty():
                db_task.set_status(self._plugins.get(), FINISHED)
            self._log.critical(f"Main tracking system is Broken with error {e}")
            raise e
        self._log.debug("Main tracking system is done")

    def _main_tracking_loop(self):
        while True:
            # Релевантные плагины, это те, которые должны быть запущены сейчас
            try:
                self._current_plugin = self._relevant_plugin()
                db_task.create(self._current_plugin)
            except ValueError as e:
                self._log.info(e)
                time.sleep(5)
                continue

            self._log.info(f'Received new plugin for Processing. name: {self._current_plugin.repository}')

            try:
                self._start_task(self._prepared_plugin(self._current_plugin))
            except UnknownObjectException | RateLimitExceededException as e:
                # Ошибка возникающая при ошибке загрузке плагина
                self._broke_current_task(e)
            except Exception as e:
                # Иная ошибка задачи
                self._broke_current_task(e)
                self._log.exception(e)
            else:
                self._log.info(f'Plugin {self._current_plugin.repository} is done successfully')
            finally:
                # Пауза перед следующей итерацией
                time.sleep(1)
                continue

    def _relevant_plugin(self) -> SPP_plugin:
        return db_plugin.relevant_plugin()

    def _prepared_plugin(self, plugin: SPP_plugin) -> GIT_Plugin:
        _plugin = GIT_Plugin(plugin)
        return _plugin

    def _broke_current_task(self, error: Exception):
        db_task.broke(self._current_plugin)
        self._log.error(f'Plugin {self._current_plugin.repository} is done with Error: {error}')

    def _start_task(self, plugin: GIT_Plugin):
        task = SPP_Parser_Task(plugin)
        task.run()
