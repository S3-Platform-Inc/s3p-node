from __future__ import annotations

from typing import TYPE_CHECKING

from src.spp.task.status import WORKING
from src.spp.task.module import get_module_by_name
from .spp_pipeline_task import SppPipelineTask

if TYPE_CHECKING:
    from src.spp.types import SPP_document, SppTask
    from src.spp.plugin.gitplugin import GitPlugin


class SppPayloadTask(SppPipelineTask):
    """
    Задача (Task) с нагрузкой (Payload). Расширенная версия задачи с постобработкой.
    """

    def __init__(self, task: SppTask, plugin: GitPlugin):
        super().__init__(task, plugin)

        self._plugin: GitPlugin = plugin
        ...

    def run(self):
        self.upload_status(WORKING)
        self._main()

    def _main(self):
        # Запуск нагрузки и ожидаение его работы

        # DRAFT
        self._bus.documents.data = self._payload()
        # self._bus.documents.data = []
        self._cycle()

    def _payload(self) -> list[SPP_document]:
        init = {}

        for entry_obj in self._plugin.config.payload.entry_params:
            if entry_obj.type.lower() == 'module':
                # Загружает класс модуля
                init[entry_obj.key] = get_module_by_name(entry_obj.value)()
            elif entry_obj.type.lower() == 'file':
                # Загружает файл в bytes-like представлении
                init[entry_obj.key] = self._plugin.file(entry_obj.value)
            elif entry_obj.type.lower() == 'const':
                # Передает константу из конфигурации
                init[entry_obj.key] = entry_obj.value
            else:
                raise ValueError(f'Entry object type as {entry_obj.type} don`t prosecuting')

        # Затем запускается модуль
        # DRAFT не подтягивается
        payload = self._plugin.payload(**init)

        return payload.__getattribute__(self._plugin.config.payload.entry_point)()

    ...
