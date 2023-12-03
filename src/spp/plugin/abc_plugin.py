from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.spp.plugin.config import Config
    from src.spp.types import SPP_plugin
    import zipfile


class ABC_Plugin(metaclass=ABCMeta):
    """
    Класс, представляющий плагин.
    """
    metadata: SPP_plugin

    _payload: Callable = None
    _config: Config

    BASE_PLUGIN_ARCHIVE_DIR_PATH: str  # Абсолютный путь до архива плагинов
    PLUGIN_CATALOG_NAME: str  # Имя каталога плагина. Нужен для проверки на уже существующее имя.
    PAYLOAD_FILENAME: str | None  # Мия файла нагрузки (логики)
    PAYLOAD_REPO_FILENAME: str | None  # Имя файла нагрузки (логики) в репозитории
    CONFIG_REPO_FILENAME: str  # Имя файла конфигурации в репозитории
    zip_repository: zipfile.ZipFile

    @property
    @abstractmethod
    def payload(self): ...

    @property
    @abstractmethod
    def config(self): ...

    @abstractmethod
    def __del__(self):
        """
        Метод вызывается при уничтожении объекта.

        Его задача удалить временный каталог с файлами плагина
        """
        # Требуется удалить каталог этого плагина
        ...

    ...
