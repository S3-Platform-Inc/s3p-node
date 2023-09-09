from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SPP_plugin


@dataclass
class SPP_task:
    """
    Структура Задачи платформы.
    """
    id: int | None
    time_next_launch: datetime | None
    plugin: SPP_plugin
    last_finish_time: datetime | None
    status_code: int
