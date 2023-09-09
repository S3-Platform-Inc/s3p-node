from dataclasses import dataclass


@dataclass
class Task:
    """
    :Task
        - logging
        - Условие активации
    """
    log_mode: int  # DEBUG, INFO, CRITICAL
    restart_time: str  # Время перезапуска в секундах
