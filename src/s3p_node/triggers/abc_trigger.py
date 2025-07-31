import logging
from abc import ABC

from s3p_sdk.types import S3PTask, S3PNode


class AbstractTrigger(ABC):
    """
    Abstract Trigger
    """
    _config: S3PNode
    _logger: logging.Logger

    def __next__(self) -> S3PTask:
        return self._task()

    def __iter__(self):
        return self

    def _task(self) -> S3PTask:
        ...
