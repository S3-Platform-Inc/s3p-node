from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SppPlugin, SppRefer


@dataclass
class SppTask:
    """
    Структура Задачи платформы.
    """
    id: int
    session_id: int
    status: int | None
    plugin: SppPlugin
    refer: SppRefer
