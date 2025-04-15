import logging
from abc import ABC
from time import sleep

from multipledispatch import dispatch
from s3p_sdk.types import S3PNode
from threading import Thread

from .brokers.database import Node


class AbstractHeartbeat(ABC):
    """
    Abstract class of Heartbeat
    """
    _interval: int
    _config: S3PNode
    _logger: logging.Logger

    def run(self):
        Node.init(self._config)
        daemon = Thread(target=self._alive, daemon=True, name='Monitor')
        daemon.start()

    def _alive(self):
        while True:
            self._logger.debug(f'Monitor: spp-node named: {self._config.name} is alive. session: {self._config.session}')
            Node.alive(self._config)
            sleep(self._interval)


class DBHeartbeat(AbstractHeartbeat):
    """
    HeartBeat implementation
    """

    @dispatch(S3PNode, int)
    def __init__(self, config: S3PNode, interval: int):
        """
        Primary constructor
        """
        self._config = config
        self._interval = interval
        self._logger = logging.getLogger(self.__class__.__name__)

    @dispatch(S3PNode)
    def __init__(self, config: S3PNode):
        """
        default interval: 5 seconds
        """
        self.__init__(config, 5)
