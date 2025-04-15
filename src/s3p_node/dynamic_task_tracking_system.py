from __future__ import annotations

import multiprocessing
from logging import getLogger
from typing import TYPE_CHECKING

from .plugin.abc_plugin import AbcPlugin
from .plugin.gitplugin import GitPlugin
from .brokers.database import Task as dbTask
from .plugin.s3plugin import S3Plugin
from .task.types.spp_payload_task import SppPayloadTask
from .triggers.abc_trigger import AbstractTrigger

if TYPE_CHECKING:
    from s3p_sdk.types import S3PNode, S3PTask


class DynamicTaskTrackingSystem(multiprocessing.Process):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _current_task: S3PTask | None
    _trigger: AbstractTrigger

    def __init__(self, node: S3PNode, trigger: AbstractTrigger):
        super().__init__()
        self._log = getLogger()
        self._node = node
        self._current_task = None
        self._trigger = trigger

    def run(self):
        self._log.debug("Main tracking system is start")
        try:
            self._main_tracking_loop()
        except Exception as e:
            if self._current_task:
                self._broke_task(e)
            self._log.critical(f"Main tracking system is Broken with error {e}")
            raise e
        self._log.debug("Main tracking system is done")

    def _main_tracking_loop(self):
        for task in self._trigger:
            self._current_task = task
            try:
                self._start_task(self._prepared_plugin(task))
            except Exception as e:
                self._broke_task(e)
                self._log.error(e)
                print(e)
            else:
                self._finish_task()

    @staticmethod
    def _prepared_plugin(task: S3PTask) -> AbcPlugin:
        _plugin = S3Plugin(task.plugin)
        return _plugin

    def _broke_task(self, error: Exception):
        dbTask.broke(self._node, self._current_task, error)
        self._log.error(f'Plugin {self._current_task.plugin.repository} is done with Error: {error}')

    def _finish_task(self):
        dbTask.finish(self._node, self._current_task)
        self._log.info(f'Plugin {self._current_task.plugin.repository} is done successfully')

    def _start_task(self, plugin: AbcPlugin | GitPlugin):
        task = SppPayloadTask(self._current_task, plugin)
        task.run()
