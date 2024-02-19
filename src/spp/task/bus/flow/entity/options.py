"""
Поток № (1) шины

Объект сущности потока шины SPP, содержащий все настройки для модулей задачи
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from ..flow import Flow

if TYPE_CHECKING:
    from src.spp.plugin.config.schemes import Module


class SppFeOptions(Flow):
    _options: tuple[Module, ...]

    def __init__(self, module_options: tuple[Module, ...]):
        super().__init__()

        self._options = module_options
        ...

    def options(self, module_name) -> Module:
        """
        Возвращает параметры по названию модуля
        :param module_name:
        :type module_name:
        :return:
        :rtype:
        """
        for module in self._options:
            if module.name == module_name:
                return module

        # Нужно сделать свою ошибку
        # https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/issues/31#issuecomment-1621309325
        raise ModuleNotFoundError(f'{module_name}')
