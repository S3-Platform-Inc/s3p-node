from __future__ import annotations

import logging
import os
from time import sleep
from threading import Thread

from .brokers.database import Node
from .dynamic_task_tracking_system import DynamicTaskTrackingSystem
from .types import SppNode


class SPPApp:
    """
    SPPApp (Source Parser Platform)
    """

    _DTT_subsystem: DynamicTaskTrackingSystem

    def __init__(self):
        # !!!WARNING Должна быть проверка платформы и всех внешних подключений.

        # Подготовка задач
        self._log = logging.getLogger()
        self.sppNode = SppNode(
            id=None,
            name=str(os.getenv('NODE_NAME')),
            ip=str(os.getenv('NODE_IP')),
            config={
                'plugins': {
                    'types': str(os.getenv('NODE_TYPES')).split(', ')
                }
            },
            session=None
        )

        self._connect()
        self._DTT_subsystem = DynamicTaskTrackingSystem(self.sppNode)
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
            self._log.debug(f'Monitor: spp-node named: {self.sppNode.name} is alive. session: {self.sppNode.session}')
            Node.alive(self.sppNode)
            sleep(interval)

    def _connect(self):
        Node.init(self.sppNode)
        daemon = Thread(target=self._alive, daemon=True, name='Monitor')
        daemon.start()
