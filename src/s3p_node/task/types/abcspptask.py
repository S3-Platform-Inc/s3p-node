from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.s3p_node.plugin.abc_plugin import AbcPlugin
    from s3p_sdk.types import S3PTask


class AbcSppTask(metaclass=ABCMeta):
    """
    Абстрактный класс задачи платформы.
    """

    _task: S3PTask
    _plugin: AbcPlugin
    _log: logging.Logger
    _status: int

    @property
    @abstractmethod
    def status(self): ...

    @abstractmethod
    def run(self): ...

    ...
