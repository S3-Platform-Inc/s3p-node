from __future__ import annotations

import multiprocessing
from logging import getLogger
from typing import TYPE_CHECKING

from typing_extensions import override

from .abc_system import AbstractSystem
from src.s3p_node.plugin.s3plugin import S3Plugin
from src.s3p_node.triggers.abc_trigger import AbstractTrigger

if TYPE_CHECKING:
    from s3p_sdk.types import S3PNode, S3PTask


@override
class DynamicTaskTrackingSystem(multiprocessing.Process, AbstractSystem):
    """
    Система отслеживания состояний задач и контроля за ними.
    """

    _trigger: AbstractTrigger

    def __init__(self, node: S3PNode, trigger: AbstractTrigger):
        super().__init__()
        self._node = node
        self._task = None
        self._trigger = trigger

    @override
    def run(self):
        _log = getLogger()
        _log.debug("Main tracking system is start")
        try:
            for task in self._trigger:
                self._task = task
                self.cover(
                    S3Plugin(task.plugin)
                )
        except Exception as e:
            if self._task:
                self._broke(e)
            _log.critical(f"Main tracking system is Broken with error {e}")
            raise e
        _log.debug("Main tracking system is done")
