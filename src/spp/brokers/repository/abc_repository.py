from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.spp.plugin.abc_plugin import AbcPlugin
    from src.spp.types import SppTask


class AbcRepository(metaclass=ABCMeta):
    """
    Абстрактный класс репозитория
    """

    # @property
    # @abstractmethod
    # def status(self): ...
    #
    # @abstractmethod
    # def run(self): ...

    ...
