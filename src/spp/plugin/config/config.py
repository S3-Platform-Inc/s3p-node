from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .schemes import Task, Parser, Middleware


@dataclass
class Config:
    """
    :source name: Уникальное имя источника, за который отвечает плагин

    :Task
        - logging
        - Условие активации

    :Parser: optional
        - Уникальное имя источника
        - Имя файла парсера
        - Имя класса парсера и точки входа
        - доп методы: optional

    :Middleware
        - Добавления модуля постобработки
        - Установки критичности
        - Дополнительный поток
    """

    source_name: str
    task: Task
    middleware: Middleware
    parser: Parser | None
    ...
