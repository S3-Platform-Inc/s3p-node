from __future__ import annotations

import importlib.util
import io
import logging
import os
import zipfile
from typing import Callable, TYPE_CHECKING

import requests
from github import Github, RateLimitExceededException, UnknownObjectException

from .abc_plugin import ABC_Plugin
from .config import Config
from .wrong_spp_language_parse import WRONG_SPP_Language_Parse

if TYPE_CHECKING:
    from github.GitRelease import GitRelease
    from spp.types import SPP_plugin, ABC_Plugin_Parser


class GIT_Plugin(ABC_Plugin):

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

    def __del__(self):
        # Delete documents
        # Нужно подумать, стоит ли хранить прошлые версии !!
        # plugin_dir = os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)
        # shutil.rmtree(plugin_dir, ignore_errors=True)
        ...

    def __init__(self, meta: SPP_plugin):
        self.metadata = meta

        self._log = logging.Logger(self.__class__.__name__)
        self._parser = None
        self._config = None
        self._SPPFILERX = os.environ.get('SPP_PLUGIN_CONFIG_FILENAME')
        self.BASE_PLUGIN_ARCHIVE_DIR_PATH = os.environ.get('SPP_ABSOLUTE_PATH_TO_PLUGIN_ARCHIVE')

        try:
            # Получение последнего релиза
            self.latest_release = self._last_release()
            # Загрузка zip-архива релиза
            self.zip_repository = self._zip_latest_release()
            # Тут нужно оформить проверку на обновление плагина. А после решать, скачивать или нет.

            # Заполнение констант из zip-релиза
            self._fill_plugin_const()

        except RateLimitExceededException as e:
            # Rate Limit исчерпан
            self._log.exception(e)
            raise e
        except UnknownObjectException as e:
            # не получилось найти последний релиз в репозитории
            self._log.exception('Plugin repository does not contain a release')
            raise e

    @property
    def parser(self):
        if self._parser is None:
            path_to_local_parser = os.path.join(
                os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME),
                self.config.parser.file_name + '.py'
            )
            if not os.path.isfile(path_to_local_parser):
                self._download_plugin_files()
            self._parser: ABC_Plugin_Parser = self._parser_class_from_file(path_to_local_parser)

        return self._parser

    @property
    def config(self):
        if self._config is None:
            # Загрузка конфигурации из zip-репозитория
            config: Config = self.parse_config(self.zip_repository.read(self.SPPFILE_REPO_FILENAME).decode())
            self._config = config

        return self._config

    def _download_plugin_files(self):
        # Загрузить конфиг и парсер
        self._extract_file_from_zip_release(self.zip_repository, self.SPPFILE_REPO_FILENAME)
        self._extract_file_from_zip_release(self.zip_repository, self.PARSER_REPO_FILENAME)

    def _zip_latest_release(self) -> zipfile.ZipFile | Exception:
        """
        Возвращает zip архив последнего релиза плагина
        :return:
        :rtype:
        """
        if not self.latest_release:
            self._log.exception('Plugin repository does not contain a release')
            raise UnknownObjectException(f'self.latest_release не загружен')
        zipBytes = requests.get(self.latest_release.zipball_url).content
        return zipfile.ZipFile(io.BytesIO(zipBytes))

    def _extract_file_from_zip_release(self, repo: zipfile.ZipFile, filename: str):
        repo.extract(filename, self.BASE_PLUGIN_ARCHIVE_DIR_PATH)
        ...

    def _parser_class_from_file(self, path: str) -> ABC_Plugin_Parser | Callable:
        spec = importlib.util.spec_from_file_location("SPP.spp_plugin." + self.config.parser.file_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_parser = module.__dict__.__getitem__(self.config.parser.class_name)
        parser_class = plugin_parser
        return parser_class

    def _fill_plugin_const(self):
        """
        Метод занимается заполнением констант плагина:
        -   SPPFILE_REPO_FILENAME   :   Полное имя SPPfile в zip-релизе
        -   PLUGIN_CATALOG_NAME     :   Имя root-каталога релиза
        -   PARSER_REPO_FILENAME    :   Полное имя файла парсера в zip-релизе

        Чтобы получить PLUGIN_CATALOG_NAME, нужно найти в списке имя, принадлежащее директории, в котором бы был только один символ `/`
        Example:
                                                           {Вложенная папка}
            [no] CuberHuber-NSPK-DI-SPP-plugin-nist-092ba29/spp/rep/

            [yes] CuberHuber-NSPK-DI-SPP-plugin-nist-092ba29/
        """
        for name in self.zip_repository.namelist():
            # Получение полного имени конфигурационного файла в zip-репозитории
            if '/SPPfile' in name:
                self.SPPFILE_REPO_FILENAME = name
            # Получение имени root-каталога релиза в zip-репозитории
            elif name.endswith('/') and name.count('/') == 1:
                self.PLUGIN_CATALOG_NAME = name
        for name in self.zip_repository.namelist():
            if f'/{self.config.parser.file_name}.py' in name:
                self.PARSER_REPO_FILENAME = name

    def _last_release(self) -> GitRelease:
        repository = Github().get_repo(self.metadata.repository)
        return repository.get_latest_release()

    def parse_config(self, config: str) -> Config | Exception:
        config: Config = WRONG_SPP_Language_Parse(config).config()
        return config

    def __eq__(self, other):
        if isinstance(other, GIT_Plugin):
            return self.metadata == other.metadata
        return False
