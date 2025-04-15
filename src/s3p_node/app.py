from __future__ import annotations

import logging
import os
from pathlib import Path

from .config.node import NodeConfig
from .dynamic_task_tracking_system import DynamicTaskTrackingSystem
from .dbheartbeat import DBHeartbeat
from .triggers.push_trigger import PushTrigger


class App:
    """
    S3P App (Source Parser Platform)
    """

    _subsystem: DynamicTaskTrackingSystem

    def __init__(self):
        # !!!WARNING Должна быть проверка платформы и всех внешних подключений.

        # Подготовка задач
        self._log = logging.getLogger()
        self._node = NodeConfig(Path(__file__).parent.parent.parent / 'node.yaml')

        self._subsystem = DynamicTaskTrackingSystem(
            self._node.content(),
            PushTrigger(self._node.content(), 5),
        )
        self._heartbeat = DBHeartbeat(self._node.content(), int(os.getenv('ALIVE_INTERVAL')))

    def run(self) -> None:
        """
        Запуск узла S3P
        """
        self._log.info('S3P start')
        self._heartbeat.run()
        self._subsystem.start()
        self._subsystem.join()
        self._log.info('S3P done')

    def health(self) -> bool:
        """
        Node health checking
        """
        ...