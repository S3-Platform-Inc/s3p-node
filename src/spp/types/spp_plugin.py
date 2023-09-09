from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class SPP_plugin:
    """
    Структура плагина платформы.
    """
    plugin_id: int | None
    repository: str
    active: bool
    pub_date: datetime | None
