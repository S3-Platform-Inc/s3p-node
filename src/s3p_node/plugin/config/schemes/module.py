from dataclasses import dataclass


@dataclass
class Module:
    """
    :Middleware
        - Порядок запуска модуля
        - Добавления модуля постобработки
        - Установки критичности
        - Дополнительный поток
        - Необходимость в шине для работы
    """
    order: int | None
    name: str
    critical: bool
    options: dict | None
    is_bus: bool | None
