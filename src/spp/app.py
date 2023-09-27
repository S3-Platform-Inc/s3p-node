from __future__ import annotations

import logging

from .dynamic_task_tracking_system import DynamicTaskTrackingSystem


class SPPApp:
    """
    SPPApp (Source Parser Platform)
    """

    _DTT_subsystem: DynamicTaskTrackingSystem

    def __init__(self):
        # !!!WARNING Должна быть проверка платформы и всех внешних подключений.

        # Подготовка задач
        self._log = logging.getLogger()
        self._DTT_subsystem = DynamicTaskTrackingSystem()
        ...

    def run(self):
        self._log.info('SPP start')
        self._DTT_subsystem.start()
        self._DTT_subsystem.join()
        self._log.info('SPP done')

    ...
