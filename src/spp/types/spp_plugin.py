from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True)
class SppPlugin:
    """
    Структура плагина платформы.
    """
    id: int | None
    repository: str
    active: bool
    loaded: datetime | None
    config: dict | None
    type: str
