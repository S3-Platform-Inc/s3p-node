from __future__ import annotations

import importlib.util
import io
import logging
import os
import shutil
import zipfile
from typing import Callable, TYPE_CHECKING

import requests
from github import Github, GithubException, RateLimitExceededException, UnknownObjectException

from .abc_plugin import ABC_Plugin
from spp.plugin.wrong_spp_language_parse import WRONG_SPP_Language_Parse

if TYPE_CHECKING:
    from .config import Config
    from spp.types import SPP_plugin, ABC_Plugin_Parser


class GIT_Plugin(ABC_Plugin):

    def __del__(self):
        # Delete documents
        # Нужно подумать, стоит ли хранить прошлые версии !!
        # plugin_dir = os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)
        # shutil.rmtree(plugin_dir, ignore_errors=True)
        ...

    def __init__(self, meta: SPP_plugin):
        self.metadata = meta

        self._log = logging.Logger(self.__class__.__name__)

        self._SPPFILERX = os.environ.get('SPP_PLUGIN_CONFIG_FILENAME')
        self.BASE_PLUGIN_ARCHIVE_DIR_PATH = os.environ.get('SPP_ABSOLUTE_PATH_TO_PLUGIN_ARCHIVE')

        try:
            self.zip_repository = self._zip_latest_release()

            # Тут нужно оформить проверку на обновление плагина. А после решать, скачивать или нет.

            for name in self.zip_repository.namelist():
                if '/SPPfile' in name:
                    self.SPPFILE_REPO_FILENAME = name
                elif name.endswith('/'):
                    self.PLUGIN_CATALOG_NAME = name

            # Загрузить конфигурацию
            config: Config = self.parse_config(self.zip_repository, self.SPPFILE_REPO_FILENAME)
            self._config = config

            for name in self.zip_repository.namelist():
                if f'/{self._config.parser.file_name}.py' in name:
                    self.PARSER_REPO_FILENAME = name

            ...
        except RateLimitExceededException as e:
            # Rate Limit исчерпан
            self._log.exception(e)
            raise e
        except UnknownObjectException as e:
            # не получилось найти последний релиз в репозитории
            self._log.exception('Plugin repository does not contain a release')
            raise e
        except Exception as e:
            # [ERROR] Невозможно получения плагина
            raise NotImplemented(e)
        else:
            ...

    @property
    def parser(self):
        if not self._parser:
            path_to_local_parser = os.path.join(
                os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME),
                self.config.parser.file_name + '.py'
            )
            if os.path.isfile(path_to_local_parser):
                self._parser: ABC_Plugin_Parser = self._parser_class_from_file(path_to_local_parser)
            else:
                self._load()

        return self._parser

    def _load(self):
        # Загрузить конфиг и парсер
        self._load_file(self.zip_repository, self.SPPFILE_REPO_FILENAME)
        self._load_file(self.zip_repository, self.PARSER_REPO_FILENAME)

        path_to_local_parser = os.path.join(
            os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME),
            self.config.parser.file_name + '.py'
        )

        self._parser: ABC_Plugin_Parser = self._parser_class_from_file(path_to_local_parser)
        ...

    def _zip_latest_release(self) -> zipfile.ZipFile | Exception:
        """
        Возвращает zip архив последнего релиза плагина
        :return:
        :rtype:
        """
        repository = Github().get_repo(self.metadata.repository)
        latest_release = repository.get_latest_release()
        zipBytes = requests.get(latest_release.zipball_url).content
        return zipfile.ZipFile(io.BytesIO(zipBytes))

    def _load_file(self, repo: zipfile.ZipFile, filename: str):
        repo.extract(filename, self.BASE_PLUGIN_ARCHIVE_DIR_PATH)
        ...

    def _parser_class_from_file(self, path: str) -> ABC_Plugin_Parser | Callable:
        spec = importlib.util.spec_from_file_location("SPP.spp_plugin." + self.config.parser.file_name, path)
        module = importlib.util.module_from_spec(spec)
        # sys.modules["SPP.spp_plugin." + parsername] = module
        spec.loader.exec_module(module)

        plugin_parser = module.__dict__.__getitem__(self.config.parser.class_name)
        parser_class = plugin_parser
        return parser_class

    def parse_config(self, repo: zipfile.ZipFile, config_name: str) -> Config | Exception:
        # Чтение
        text_config = repo.read(config_name).decode()
        config: Config = WRONG_SPP_Language_Parse(text_config).config()
        return config

        # Проверка
        # if False:
        #     ...
        # else:
        #     # [ERROR] Плагин не соответствует требованиям. Ошибка в SPPfile
        #
        #     # указать сроку с ошибкой
        #     raise NotImplemented

    def __eq__(self, other):
        if isinstance(other, GIT_Plugin):
            return self.metadata == other.metadata
        return False
