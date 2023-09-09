from dataclasses import dataclass


@dataclass
class Module:
    """
    :Middleware
        - Добавления модуля постобработки
        - Установки критичности
        - Дополнительный поток
    """
    name: str
    options: tuple
    critical: bool
