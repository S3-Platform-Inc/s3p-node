from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from spp.plugin.abc_plugin import ABC_Plugin
    from src.spp.types import SPP_source


class ABC_SPP_Task(metaclass=ABCMeta):
    """
    Абстрактный класс задачи платформы.
    """

    _plugin: ABC_Plugin
    _log: logging.Logger
    _source: SPP_source
    _status: int

    @property
    @abstractmethod
    def status(self): ...

    @abstractmethod
    def run(self): ...

    ...
