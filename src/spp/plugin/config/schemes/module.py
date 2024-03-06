from dataclasses import dataclass


@dataclass
class Module:
    """
    :Middleware
        - Порядок запуска модуля
        - Добавления модуля постобработки
        - Установки критичности
        - Дополнительный поток
    """
    order: int
    name: str
    critical: bool
    options: dict | None
