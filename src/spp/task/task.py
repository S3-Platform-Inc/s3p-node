from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from src.spp.brokers.database import Source as dbSource, Task as dbTask
from .status import NONSET, _statusToName
from .types.abcspptask import AbcSppTask

if TYPE_CHECKING:
    from src.spp.plugin.gitplugin import GitPlugin
    from src.spp.types import SPP_source


class Task(AbcSppTask):
    _plugin: GitPlugin
    _log: logging.Logger
    _source: SPP_source

    _status: int

    def __init__(self, plugin: GitPlugin, classname: str = None):
        super().__init__()
        if classname is None:
            self._log = logging.getLogger(self.__class__.__name__)
        else:
            self._log = logging.getLogger(classname)
        self._log.info("Task started")

        self._plugin = plugin
        self.upload_status(NONSET)
        self.__safe_get_source()

    @property
    def status(self):
        """
        Возвращает текущий статус работы задачи
        """
        return self._status

    def run(self): ...

    def __safe_get_source(self):
        self._source = dbSource.safe(self._plugin.config.plugin.reference_name)

    def upload_status(self, status: int):
        """
        Метод для обновления статуса в базе данных и в инстансе класса

        NONSET      0
        AWAITING    10
        PREPARING   20
        READY       30
        WORKING     40
        SUSPENDED   50
        FINISHED    60
        BROKEN      70
        :param status:
        :type status:
        """
        self._status = status
        dbTask.status_update(self._plugin.metadata, status)
        self._log.debug(f'Task {self._plugin.metadata.plugin_id} change status to {_statusToName[status]}')

    def _finish_hook(self):
        restart_interval = self._plugin.config.task.restart_interval
        dbTask.finish(self._plugin.metadata, restart_interval)
