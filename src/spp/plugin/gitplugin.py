from __future__ import annotations

import importlib.util
import io
import logging
import os
import re
import zipfile
from typing import Callable, TYPE_CHECKING, BinaryIO
from pathlib import Path

import requests
from github import Github, RateLimitExceededException, UnknownObjectException, Auth

from .abc_plugin import ABC_Plugin
from .config import Config
from .wrong_spp_language_parse import WRONG_SPP_Language_Parse

if TYPE_CHECKING:
    from github.GitRelease import GitRelease
    from src.spp.types import SPP_plugin


class GitPlugin(ABC_Plugin):
    """
    :metadata: структура плагина, получаемая от БД

    :_payload: объект нагрузки. Вызывается перед запуском постобработки.
    :_config: конфигурация.

    """

    metadata: SPP_plugin

    _payload: Callable = None
    _config: Config

    BASE_PLUGIN_ARCHIVE_DIR_PATH: str  # Абсолютный путь до архива плагинов
    PLUGIN_CATALOG_NAME: str  # Имя каталога плагина. Нужен для проверки на уже существующее имя.
    REPOSITORY_ROOT_CATALOG_NAME: str
    PAYLOAD_FILENAME: str | None
    PAYLOAD_REPO_FILENAME: str | None  # Имя файла парсера в репозитории
    CONFIG_REPO_FILENAME: str  # Имя файла конфигурации в репозитории
    zip_repository: zipfile.ZipFile

    def __del__(self):
        # Delete documents
        # Нужно подумать, стоит ли хранить прошлые версии !!
        # plugin_dir = os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)
        # shutil.rmtree(plugin_dir, ignore_errors=True)
        ...

    def __init__(self, meta: SPP_plugin):
        self.metadata = meta
        self._log = logging.Logger(self.__class__.__name__)

        self._payload = None
        self._config = None

        self._SPPFILERX = os.environ.get('SPP_PLUGIN_CONFIG_FILENAME')

        self.BASE_PLUGIN_ARCHIVE_DIR_PATH = os.environ.get('SPP_ABSOLUTE_PATH_TO_PLUGIN_ARCHIVE')
        self.PLUGIN_CATALOG_NAME = None
        self.REPOSITORY_ROOT_CATALOG_NAME = None
        self.PAYLOAD_FILENAME = None
        self.PAYLOAD_REPO_FILENAME = None
        self.CONFIG_REPO_FILENAME = None
        self.zip_repository = None

        try:
            # Получение последнего релиза
            self.latest_release = self._git_last_release()
            # Загрузка zip-архива релиза
            self.zip_repository = self._zip_latest_release()
            # Тут нужно оформить проверку на обновление плагина. А после решать, скачивать или нет.
        except RateLimitExceededException as e:
            # Rate Limit исчерпан
            self._log.exception(e)
            raise e
        except UnknownObjectException as e:
            # не получилось найти последний релиз в репозитории
            self._log.exception('Plugin repository does not contain a release')
            raise e
        else:
            # Заполнение констант из zip-релиза
            self._fill_plugin_const()
            self._extract_plugin_files()
            self._verify()

    def _path_for_filename(self, filename: str, exists: bool = False, mkdir: bool = False) -> str:
        local_path = os.path.join(
            os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME),
            filename
        )
        if mkdir:
            directory_path = re.sub(r'\/([^\/]+)$', '', local_path)
            print(directory_path)
            Path(directory_path).mkdir(parents=True, exist_ok=True)

        if exists and not os.path.isfile(local_path):
            raise FileNotFoundError(f'file {filename} not found in the plugin {self.PLUGIN_CATALOG_NAME}')
        return local_path

    @property
    def payload(self) -> Callable | Exception:
        if self._payload is None:
            self._payload = self._payload_python_class_from_file(self._path_for_filename(self.config.payload.file_name, True))

        return self._payload

    @property
    def config(self) -> Config | Exception:
        if self._config is None:
            # Загрузка конфигурации
            conf_text: str = None
            try:
                with open(self._path_for_filename(self._SPPFILERX, True), 'rb') as config_file:
                    conf_text = config_file.read().decode()
            except FileNotFoundError:
                conf_text = self.zip_repository.read(self.CONFIG_REPO_FILENAME).decode()
            finally:
                config: Config = GitPlugin._parse_config(conf_text)
                self._config = config

        return self._config

    # Нужно обдумать метод загрузки и использования файлов из плагина
    def file(self, filename: str) -> BinaryIO | io.BytesIO | Exception:
        """
        Методы возвращает файл плагина по его мени
        """
        if isinstance(filename, str):
            _path = self._path_for_filename(filename, True)
            with open(_path, 'rb') as file:
                return io.BytesIO(file.read())
        else:
            raise TypeError(f'filename must be of str type')

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

    def _extract_file_from_zip(self, filename: str, repository_filename: str):
        assert isinstance(self.PLUGIN_CATALOG_NAME, str)
        assert isinstance(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, str)

        with open(filename, 'wb') as ext_file:
            ext_file.write(self.zip_repository.read(repository_filename))

    def _payload_python_class_from_file(self, path: str) -> Callable:
        spec = importlib.util.spec_from_file_location("SPP.spp_plugin." + self.config.payload.file_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_payload = module.__dict__.__getitem__(self.config.payload.class_name)
        payload_class = plugin_payload
        return payload_class

    def  _fill_plugin_const(self):
        """
        Чтобы получить PLUGIN_CATALOG_NAME, нужно найти в списке имя, принадлежащее директории, в котором бы был только один символ `/`
        Example:
                                                           {Вложенная папка}
            [no] CuberHuber-NSPK-DI-SPP-plugin-nist-092ba29/spp/rep/

            [yes] CuberHuber-NSPK-DI-SPP-plugin-nist-092ba29/
        """
        self.PLUGIN_CATALOG_NAME = re.sub(r"^(.+)\/", "", self.metadata.repository, 0, re.MULTILINE)

        for name in self.zip_repository.namelist():
            if name.endswith('/') and name.count('/') == 1:
                self.REPOSITORY_ROOT_CATALOG_NAME = name
                self.CONFIG_REPO_FILENAME = os.path.join(self.REPOSITORY_ROOT_CATALOG_NAME, self._SPPFILERX)
                return
        raise ValueError(f'Zip release does not contain a root directory')

    def _extract_plugin_files(self):
        assert isinstance(self.REPOSITORY_ROOT_CATALOG_NAME, str)

        if not os.path.isdir(os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)):
            os.mkdir(os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME))

        for filename in self.config.plugin.filenames:
            repository_filename = os.path.join(self.REPOSITORY_ROOT_CATALOG_NAME, filename)
            self._extract_file_from_zip(self._path_for_filename(filename, mkdir=True), repository_filename)

    def _verify(self):
        """
        В плагине должен быть как минимум файл SPPfile
        """
        self._path_for_filename(self._SPPFILERX, True)

    def _git_last_release(self) -> GitRelease:
        _release: GitRelease | None = None
        auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
        with Github(auth=auth) as g:
            repository = g.get_repo(self.metadata.repository)
            _release = repository.get_latest_release()
        return _release

    @staticmethod
    def _parse_config(config: str) -> Config | Exception:
        config: Config = WRONG_SPP_Language_Parse(config).config
        return config

    def __eq__(self, other):
        if isinstance(other, GitPlugin):
            return self.metadata == other.metadata
        return False
