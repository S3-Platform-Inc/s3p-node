import logging
import time

from multipledispatch import dispatch
from s3p_sdk.types import S3PTask, S3PNode
from typing_extensions import override

from .abc_trigger import AbstractTrigger
from ..brokers.database import Task as dbTask
from ..exceptions.triggers.no_relevant_tasks import NoRelevantTasks


class PushTrigger(AbstractTrigger):
    _interval: int

    @dispatch(S3PNode, int)
    def __init__(self, config: S3PNode, interval: int):
        """Primary constructor"""
        self._interval = interval
        self._config = config
        self._logger = logging.getLogger(self.__class__.__name__)

    @dispatch(S3PNode)
    def __init__(self, config: S3PNode):
        """Default interval - 5"""
        self.__init__(config, 5)

    @override
    def __iter__(self):
        while True:
            try:
                relevant = self._task()
            except NoRelevantTasks as e:
                self._logger.debug(e)
                time.sleep(self._interval)
            else:
                self._logger.info(
                    f'Received new task for processing. ID: {relevant.plugin.id}, Name: {relevant.plugin.repository}')
                yield relevant
                time.sleep(self._interval)

    @override
    def __next__(self):
        # Either don't implement this or raise NotImplementedError
        raise NotImplementedError("Use this class as an iterable with for loops, not as an iterator with next()")

    @override
    def _task(self) -> S3PTask | Exception:
        return dbTask.relevant(self._config)
