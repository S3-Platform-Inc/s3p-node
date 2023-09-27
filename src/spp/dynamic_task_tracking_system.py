from __future__ import annotations

import multiprocessing
import time
from logging import getLogger
from typing import TYPE_CHECKING

from .plugin.git_plugin import GIT_Plugin
from .brokers.database import Plugin as db_plugin, Task as db_task
from .task.types.spp_parser_task import SPP_Parser_Task
from .task.status import BROKEN, AWAITING, FINISHED

if TYPE_CHECKING:
    from src.spp.types import SPP_plugin


class DynamicTaskTrackingSystem(multiprocessing.Process):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _plugins: multiprocessing.Queue


    def __init__(self):
        super().__init__()
        self._log = getLogger()
        self._plugins = multiprocessing.Queue()

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
            time.sleep(5)
            # Релевантные плагины, это те, которые должны быть запущены сейчас
            relevant_plugins = self._relevant_plugins()
            for _plugin in relevant_plugins:
                db_task.create(_plugin, status_code=AWAITING)
                self._plugins.put(_plugin)

            while not self._plugins.empty():
                _plugin = self._plugins.get()
                self._log.info(f'Received new plugin for Processing. name: {_plugin.repository}')
                try:
                    self._start_task(self._prepared_plugin(_plugin))
                except Exception as e:
                    db_task.set_status(_plugin, BROKEN)
                    raise e
                self._log.info(f'Plugin {_plugin.repository} is done')

    def _relevant_plugins(self) -> list[SPP_plugin]:
        return db_plugin.relevant_plugins()

    def _prepared_plugin(self, plugin: SPP_plugin) -> GIT_Plugin:
        _plugin = GIT_Plugin(plugin)
        return _plugin

    def _start_task(self, plugin: GIT_Plugin):
        task = SPP_Parser_Task(plugin)
        task.run()
