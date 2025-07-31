from abc import ABC, abstractmethod
from logging import getLogger
from typing import Optional

from s3p_sdk.types import S3PNode, S3PTask

from src.s3p_node.plugin.abc_plugin import AbcPlugin
from src.s3p_node.task.types.spp_payload_task import SppPayloadTask
from src.s3p_node.brokers.database import Task as dbTask


class AbstractSystem(ABC):

    _node: S3PNode
    _task: Optional[S3PTask]

    def cover(self, plugin: AbcPlugin):
        try:
            self._start(plugin)
        except Exception as e:
            self._broke(e)
        else:
            self._finish()

    def _start(self, plugin: AbcPlugin):
        task = SppPayloadTask(self._task, plugin)
        task.run()

    def _finish(self):
        dbTask.finish(self._node, self._task)
        getLogger(self.__class__.__name__).info(f'Plugin {self._task.plugin.repository} is done successfully')

    def _broke(self, error: Exception):
        dbTask.broke(self._node, self._task, error)
        getLogger(self.__class__.__name__).error(f'Plugin {self._task.plugin.repository} is done with Error: {error}')