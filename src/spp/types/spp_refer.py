from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class SppRefer:
    """
    Объект источника в SPP
    """
    id: int
    name: str | None
    type: str | None
    load_date: datetime | None
