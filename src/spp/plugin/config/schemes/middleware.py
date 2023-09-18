from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .module import Module


@dataclass
class Middleware:
    """
    Схема конфигурации middleware, содержащую список модулей и дополнительные потоки шины
    """
    modules: tuple[Module]
    additional_bus_entities: tuple[tuple]

    def module_by_name(self, name: str) -> Module | Exception:
        """
        Возвращает объект модуля по его имени. Если модуля нет, то выбрасывает ошибку
        :param name:
        :type name:
        :return:
        :rtype:
        """
        for module in self.modules:
            if module.name == name:
                return module

        # Ошибка модуль не найден
        raise NotImplemented(f'Module {name} has not found')
