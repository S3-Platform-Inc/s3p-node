from __future__ import annotations

from typing import TYPE_CHECKING

from .dynamic_multiprocessor_task_pool import DynamicMultiprocessorTaskPool
from .dynamic_task_tracking_system import DynamicTaskTrackingSystem

if TYPE_CHECKING:
    from spp.plugin.abc_plugin import ABC_Plugin


class SPPApp:
    """
    SPPApp (Source Parser Platform)
    """

    _plugins: list[ABC_Plugin]
    _DTT_subsystem: DynamicTaskTrackingSystem

    def __init__(self):
        # !!!WARNING Должна быть проверка платформы и всех внешних подключений.

        # Подготовка задач
        self._DTT_subsystem = DynamicTaskTrackingSystem(DynamicMultiprocessorTaskPool())
        ...

    def run(self):
        self._DTT_subsystem.start()
        self._DTT_subsystem.join()

    ...
