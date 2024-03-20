from __future__ import annotations

import multiprocessing
import time
from logging import getLogger
from typing import TYPE_CHECKING

from .plugin.abc_plugin import AbcPlugin
from .plugin.gitplugin import GitPlugin
from .brokers.database import Task as dbTask
from .task.types.spp_payload_task import SppPayloadTask

if TYPE_CHECKING:
    from src.spp.types import SppNode, SppTask


class DynamicTaskTrackingSystem(multiprocessing.Process):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _current_task: SppTask | None

    def __init__(self, spp_node: SppNode):
        super().__init__()
        self._log = getLogger()
        self._node = spp_node
        self._current_task = None

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
        while True:
            # Релевантные плагины, это те, которые должны быть запущены сейчас
            try:
                self._current_task = self._relevant()
            except ValueError as e:
                self._log.info(e)
                time.sleep(5)
                continue

            self._log.info(f'Received new plugin for Processing. name: {self._current_task.plugin.repository}')

            try:
                # Теперь SppTask получен. Нужно придумать способ подготовки задачи для запуска.
                # Можно сделать передачу SppTask в Task при инициализации. Или подготовить плагин и положить ее в
                self._start_task(self._prepared_plugin(self._current_task))
            # except UnknownObjectException | RateLimitExceededException as e:
            #     # Ошибка возникающая при ошибке загрузке плагина
            #     self._broke_current_task(e)
            #     self._log.error(e)
            #     print(e)
            except Exception as e:
                # Иная ошибка задачи
                self._broke_task(e)
                self._log.error(e)
                print(e)
            else:
                self._finish_task()
            finally:
                # Пауза перед следующей итерацией
                time.sleep(1)
                continue

    def _relevant(self) -> SppTask | Exception:
        return dbTask.relevant(self._node)

    @staticmethod
    def _prepared_plugin(task: SppTask) -> AbcPlugin:
        # Разделен класс на ABCPlugin -> Plugin -> GitPlugin
        _plugin = GitPlugin(task.plugin)
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
