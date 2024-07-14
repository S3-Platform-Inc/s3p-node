from __future__ import annotations

from typing import TYPE_CHECKING
from s3p_sdk.task.status import WORKING

from src.s3p_node.task.module import get_module_by_name
from .spp_pipeline_task import SppPipelineTask

if TYPE_CHECKING:
    from s3p_sdk.types import S3PDocument, S3PTask
    from src.s3p_node.plugin.gitplugin import GitPlugin
    from src.s3p_node.plugin.config.schemes import Module, FileObject, ConstantObject


class SppPayloadTask(SppPipelineTask):
    """
    Задача (Task) с нагрузкой (Payload). Расширенная версия задачи с постобработкой.
    """

    def __init__(self, task: S3PTask, plugin: GitPlugin):
        super().__init__(task, plugin)

        self._plugin: GitPlugin = plugin
        ...

    def run(self):
        self.logging('start')
        self.upload_status(WORKING)
        self._main()
        self.logging('done')

    def _main(self):
        # Запуск нагрузки и ожидаение его работы

        # DRAFT
        self._bus.documents.data = self._payload()
        # self._bus.documents.data = []
        self._cycle()

    def _payload(self) -> list[S3PDocument]:
        init = {}

        for entry_obj in self._plugin.config.payload.entry_params:
            if isinstance((module := entry_obj.value), Module):
                # Загружает класс модуля
                if module.is_bus:
                    # Если есть параметр is_bus, то в модуль нужно передать ссылку на шину
                    _module = get_module_by_name(module.name)(self._bus)
                else:
                    # Иначе просто вызвать
                    _module = get_module_by_name(module.name)()

                # Вызов основной логики модуля и сохранения результата
                init[entry_obj.key] = _module()
            elif isinstance((file := entry_obj.value), FileObject):
                # Загружает файл в bytes-like представлении
                init[entry_obj.key] = self._plugin.file(file.name)
            elif isinstance((const := entry_obj.value), ConstantObject):
                # Передает константу из конфигурации
                init[entry_obj.key] = const.value
            else:
                raise ValueError(f'Entry object type as {entry_obj.type} don`t prosecuting')

        # Затем запускается модуль
        # DRAFT не подтягивается
        payload = self._plugin.payload(**init)

        return payload.__getattribute__(self._plugin.config.payload.entry_point)()

    ...
