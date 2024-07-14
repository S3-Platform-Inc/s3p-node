from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.s3p_node.plugin.config import Config
    from s3p_sdk.types import S3PPlugin


class AbcPlugin(metaclass=ABCMeta):
    """
    Класс, представляющий плагин.
    """
    metadata: S3PPlugin
    _config: Config

    BASE_PLUGIN_ARCHIVE_DIR_PATH: str  # Абсолютный путь до архива плагинов
    PLUGIN_CATALOG_NAME: str  # Имя каталога плагина. Нужен для проверки на уже существующее имя.

    @property
    @abstractmethod
    def config(self) -> Config:
        ...

    @abstractmethod
    def __del__(self):
        """
        Метод вызывается при уничтожении объекта.

        Его задача удалить временный каталог с файлами плагина
        """
        # Требуется удалить каталог этого плагина
        ...

    ...
