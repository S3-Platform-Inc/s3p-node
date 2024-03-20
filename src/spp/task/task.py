from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.spp.brokers.database import Task as dbTask
from .status import PREPARING, _statusToName
from .types.abcspptask import AbcSppTask

if TYPE_CHECKING:
    from src.spp.plugin.abc_plugin import AbcPlugin
    from src.spp.types import SppTask


class Task(AbcSppTask):
    _task: SppTask
    _plugin: AbcPlugin
    _log: logging.Logger

    _status: int

    def __init__(self, task: SppTask, plugin: AbcPlugin, classname: str = None):
        super().__init__()
        if classname is None:
            self._log = logging.getLogger(self.__class__.__name__)
        else:
            self._log = logging.getLogger(classname)
        self._log.info("Task started")

        self._task = task
        self._plugin = plugin
        self.upload_status(PREPARING)

    @property
    def status(self):
        """
        Возвращает текущий статус работы задачи
        """
        return self._status

    def run(self): ...

    def upload_status(self, status: int):
        """
        Метод для обновления статуса в базе данных и в инстансе класса

        NONSET = 0
        SCHEDULED = 10
        GIVEN = 20
        PREPARING = 30
        WORKING = 40
        FINISHED = 50
        BROKEN = 60
        TERMINATED = 70
        DEACTIVATED = 80
        :param status:
        :type status:
        """
        self._status = status
        dbTask.status_update(self._task, status)
        self._log.debug(f'Task {self._plugin.metadata.id} change status to {_statusToName[status]}')
