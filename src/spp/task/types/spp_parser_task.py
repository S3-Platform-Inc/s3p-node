from __future__ import annotations

from typing import TYPE_CHECKING
from multiprocessing import current_process

from spp.task.status import WORKING
from spp.task.module import get_module_by_name
from .spp_pipeline_task import SPP_Pipeline_Task

if TYPE_CHECKING:
    from src.spp.types import SPP_document


class SPP_Parser_Task(SPP_Pipeline_Task):
    """
    Задача (Task) с парсером. Расширенная версия задачи с постобработкой.
    """

    def __init__(self, plugin):
        super().__init__(plugin)
        ...

    def run(self):
        print('run', current_process())
        self.upload_status(WORKING)
        self._main()

    def __call__(self):
        print('__call__', current_process())
        self.upload_status(WORKING)
        self._main()

    def _main(self):
        # Запуск парсера и ожидаение его работы

        # DRAFT
        # self._bus.documents.data = self._parser()
        self._bus.documents.data = []
        self._cycle()

    def _parser(self) -> list[SPP_document]:
        init = {key: get_module_by_name(value)() for key, value in
                self._plugin.config.parser.entry_keywords}

        # Затем запускается модуль
        # DRAFT не подтягивается
        parser = self._plugin.parser(**init)

        return parser.__getattribute__(self._plugin.config.parser.entry_point)()

    ...
