from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.spp.plugin.abc_plugin import AbcPlugin
    from src.spp.types import SppTask


class AbcSppTask(metaclass=ABCMeta):
    """
    Абстрактный класс задачи платформы.
    """

    _task: SppTask
    _plugin: AbcPlugin
    _log: logging.Logger
    _status: int

    @property
    @abstractmethod
    def status(self): ...

    @abstractmethod
    def run(self): ...

    ...
