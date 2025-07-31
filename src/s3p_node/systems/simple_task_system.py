import multiprocessing
from multipledispatch import dispatch
from logging import getLogger

from typing_extensions import override

from .abc_system import AbstractSystem
from src.s3p_node.brokers.database.task import Task as dbTask
from src.s3p_node.plugin.s3plugin import S3Plugin
from s3p_sdk.types import S3PNode, S3PTask


class SimpleTaskSystem(multiprocessing.Process, AbstractSystem):

    @dispatch(S3PNode, S3PTask)
    def __init__(self, node: S3PNode, task: S3PTask):
        super().__init__()
        self._task = task
        self._node = node

    @dispatch(S3PNode, int)
    def __init__(self, node: S3PNode, plugin_id: int):
        self.__init__(
            node,
            dbTask.start_session(None, plugin_id)
        )

    @override
    def run(self):
        _log = getLogger()
        _log.debug("Main tracking system is start")
        try:
            self.cover(S3Plugin(self._task.plugin))
        except Exception as e:
            if self._task:
                self._broke(e)
            _log.critical(f"Main tracking system is Broken with error {e}")
            raise e
        _log.debug("Main tracking system is done")

    @override
    def _broke(self, error: Exception):
        dbTask.broke(self._node, self._task, error)
        getLogger(self.__class__.__name__).error(f'Plugin {self._task.plugin.repository} is done with Error: {error}')
        raise Exception(f"Plugin {self._task.plugin.repository} is done with Error: {error}") from error