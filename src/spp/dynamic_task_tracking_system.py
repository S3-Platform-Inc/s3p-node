from __future__ import annotations

import time
from logging import getLogger
from multiprocessing import Process
from typing import TYPE_CHECKING

from spp.plugin.git_plugin import GIT_Plugin
from src.spp.brokers.database import Plugin as db_plugin, Task as db_task

if TYPE_CHECKING:
    from .dynamic_multiprocessor_task_pool import DynamicMultiprocessorTaskPool
    from src.spp.types import SPP_plugin
    from .plugin.abc_plugin import ABC_Plugin


class DynamicTaskTrackingSystem(Process):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _loop_restart_time: int  # в секундах
    _pool: DynamicMultiprocessorTaskPool
    _plugins: list[SPP_plugin]

    def __init__(self, dmt_pool: DynamicMultiprocessorTaskPool, loop_restart_time: int = 10):
        super().__init__()
        self._log = getLogger()
        self._loop_restart_time = loop_restart_time
        self._pool = dmt_pool

    def run(self):
        self._log.debug("Main tracking system is start")
        self._main_tracking_loop()
        self._log.debug("Main tracking system is finished")

    def t_run(self):
        self._log.debug("Main tracking system is start")
        self._main_tracking_loop()
        self._log.debug("Main tracking system is finished")

    def _main_tracking_loop(self):
        while True:
            time.sleep(self._loop_restart_time)

            # Релевантные плагины, это те, которые должны быть запущены сейчас
            self._plugins = self._relevant_plugins()

            # Очистка пула
            self._pool.clear()

            for plugin in self._plugins:
                self._create_task(self._prepared_plugin(plugin))

    def _relevant_plugins(self) -> list[SPP_plugin]:
        return db_plugin.relevant_plugins()

    def _prepared_plugin(self, plugin: SPP_plugin) -> ABC_Plugin:
        _plugin = GIT_Plugin(plugin)
        _plugin.load()
        return _plugin

    def _create_task(self, plugin: ABC_Plugin):
        self._pool.add(plugin)
        # db_task.create(plugin.metadata)
        self._pool.start(plugin)
