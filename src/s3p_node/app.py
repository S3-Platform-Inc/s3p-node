from __future__ import annotations

import logging
import multiprocessing
import os
from pathlib import Path

from multipledispatch import dispatch
from s3p_sdk.types import S3PNode

from .config.node import NodeConfig
from .dbheartbeat import DBHeartbeat
from .systems.dynamic_task_tracking_system import DynamicTaskTrackingSystem
from .systems.simple_task_system import SimpleTaskSystem
from .triggers.push_trigger import PushTrigger


class App:
    """
    S3P App (Source Parser Platform)
    """

    _subsystem: multiprocessing.Process

    @dispatch(S3PNode, multiprocessing.Process)
    def __init__(self, node: S3PNode, system: multiprocessing.Process):
        self._log = logging.getLogger()
        self._node = node
        self._subsystem = system

        self._heartbeat = DBHeartbeat(self._node, int(os.getenv('ALIVE_INTERVAL')))

    @dispatch()
    def __init__(self):
        node = NodeConfig(Path(__file__).parent.parent.parent / 'node.yaml').content()
        self.__init__(
            node,
            DynamicTaskTrackingSystem(
                node,
                PushTrigger(node, 5),
            )
        )

    @dispatch(int)
    def __init__(self, plugin_id: int):
        node = NodeConfig(Path(__file__).parent.parent.parent / 'node.yaml').content()
        self.__init__(
            node,
            SimpleTaskSystem(
                node,
                plugin_id
            )
        )

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
        S3 Platform health checking
        """
        ...
