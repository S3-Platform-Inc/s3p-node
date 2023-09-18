from __future__ import annotations

import multiprocessing
import time
from logging import getLogger
from typing import TYPE_CHECKING

from src.spp.plugin.git_plugin import GIT_Plugin
from src.spp.brokers.database import Plugin as db_plugin, Task as db_task
from src.spp.task.types.spp_parser_task import SPP_Parser_Task
from src.spp.task.status import PREPARING, SUSPENDED, READY, WORKING, AWAITING, FINISHED

if TYPE_CHECKING:
    from src.spp.types import SPP_plugin
    from src.spp.plugin.abc_plugin import ABC_Plugin


class DynamicTaskTrackingSystem(multiprocessing.Process):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _plugins: list[SPP_plugin]

    def __init__(self):
        super().__init__()
        self._log = getLogger()

    def run(self):
        self._log.debug("Main tracking system is start")
        try:
            self._main_tracking_loop()
        except Exception as e:
            for plugin in self._plugins:
                db_task.set_status(plugin, FINISHED)
            self._log.critical(f"Main tracking system is Broken with error {e}")
            raise e
        self._log.debug("Main tracking system is done")

    def _main_tracking_loop(self):
        while True:
            time.sleep(5)
            # Релевантные плагины, это те, которые должны быть запущены сейчас
            self._plugins = self._relevant_plugins()
            for plugin in self._plugins:
                db_task.create(plugin, status_code=AWAITING)
                # db_task.set_status(plugin, AWAITING)

            for plugin in self._plugins:
                self._log.info(f'Received new plugin for Processing. name: {plugin.repository}')
                self._start_task(self._prepared_plugin(plugin))
                self._log.info(f'Plugin {plugin.repository} is done')

    def _relevant_plugins(self) -> list[SPP_plugin]:
        return db_plugin.relevant_plugins()

    def _prepared_plugin(self, plugin: SPP_plugin) -> ABC_Plugin:
        _plugin = GIT_Plugin(plugin)
        # _plugin.load()
        return _plugin

    def _start_task(self, plugin: ABC_Plugin):
        task = SPP_Parser_Task(plugin)
        task.run()
