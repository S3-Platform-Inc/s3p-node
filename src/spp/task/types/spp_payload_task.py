from __future__ import annotations

from typing import TYPE_CHECKING

from spp.task.status import WORKING
from spp.task.module import get_module_by_name
from .spp_pipeline_task import SPP_Pipeline_Task

if TYPE_CHECKING:
    from src.spp.types import SPP_document


class SPP_Payload_Task(SPP_Pipeline_Task):
    """
    Задача (Task) с нагрузкой (Payload). Расширенная версия задачи с постобработкой.
    """

    def __init__(self, plugin):
        super().__init__(plugin)
        ...

    def run(self):
        self.upload_status(WORKING)
        self._main()
        self._finish_hook()

    def _main(self):
        # Запуск нагрузки и ожидаение его работы

        # DRAFT
        self._bus.documents.data = self._payload()
        # self._bus.documents.data = []
        self._cycle()

    def _payload(self) -> list[SPP_document]:
        init = {key: get_module_by_name(value)() for key, value in
                self._plugin.config.payload.entry_keywords}

        # Затем запускается модуль
        # DRAFT не подтягивается
        payload = self._plugin.payload(**init)

        return payload.__getattribute__(self._plugin.config.payload.entry_point)()

    ...
