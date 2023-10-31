from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.spp.plugin.config import Config
    from src.spp.types import ABC_Plugin_Parser, SPP_plugin
    from github.GitRelease import GitRelease
    import zipfile



class ABC_Plugin(metaclass=ABCMeta):
    """
    Класс, представляющий плагин.
    """
    metadata: SPP_plugin

    _parser: ABC_Plugin_Parser | Callable = None
    _config: Config

    BASE_PLUGIN_ARCHIVE_DIR_PATH: str  # Абсолютный путь до архива плагинов
    PLUGIN_CATALOG_NAME: str  # Имя каталога плагина. Нужен для проверки на уже существующее имя.
    PARSER_FILENAME: str | None
    PARSER_REPO_FILENAME: str | None  # Имя файла парсера в репозитории
    SPPFILE_REPO_FILENAME: str  # Имя файла конфигурации в репозитории
    zip_repository: zipfile.ZipFile
    latest_release: GitRelease

    @property
    @abstractmethod
    def parser(self): ...

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
