from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass
class SPP_source:
    """
    Объект источника в SPPApp
    """
    src_id: int
    name: str
    config: dict
    sphere: str
    load_date: datetime
