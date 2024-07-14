from __future__ import annotations

import logging
import os
from time import sleep
from threading import Thread
from s3p_sdk.types import S3PNode

from .brokers.database import Node
from .dynamic_task_tracking_system import DynamicTaskTrackingSystem


class S3PApp:
    """
    SPPApp (Source Parser Platform)
    """

    _DTT_subsystem: DynamicTaskTrackingSystem

    def __init__(self):
        # !!!WARNING Должна быть проверка платформы и всех внешних подключений.

        # Подготовка задач
        self._log = logging.getLogger()
        self._node = S3PNode(None, str(os.getenv('NODE_NAME')), str(os.getenv('NODE_IP')), {
            'plugins': {
                'types': str(os.getenv('NODE_TYPES')).split(', ')
            }
        }, None)

        self._connect()
        self._DTT_subsystem = DynamicTaskTrackingSystem(self._node)
        ...

    def run(self):
        """
        Запуск узла SPP
        :return:
        """
        self._log.info('SPP start')
        self._DTT_subsystem.start()
        self._DTT_subsystem.join()
        self._log.info('SPP done')

    def _alive(self):
        interval = int(os.getenv('ALIVE_INTERVAL'))
        while True:
            self._log.debug(f'Monitor: spp-node named: {self._node.name} is alive. session: {self._node.session}')
            Node.alive(self._node)
            sleep(interval)

    def _connect(self):
        Node.init(self._node)
        daemon = Thread(target=self._alive, daemon=True, name='Monitor')
        daemon.start()
