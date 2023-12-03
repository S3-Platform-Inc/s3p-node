from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schemes import Task, Payload, Middleware, Plugin


@dataclass
class Config:
    """
    :plugin: настройки плагина

    :task: настройки задачи

    :middleware: настройки постобработки

    :payload: optional - настройки нагрузки
    """
    plugin: Plugin
    task: Task
    middleware: Middleware
    payload: Payload | None
