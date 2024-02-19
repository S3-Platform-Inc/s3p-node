from dataclasses import dataclass


@dataclass
class Task:
    """
    :Task
        - logging
        - Условие активации
    """
    log: int  # DEBUG, INFO, ERROR, CRITICAL
    trigger: str  # Interval type: Строка интервала перезапуска задачи
