"""
gitplugin.py
"""

from __future__ import annotations

import importlib.util
import io
import os
import re
import zipfile
from pathlib import Path
from typing import Callable, TYPE_CHECKING, BinaryIO

import requests
from github import Github, RateLimitExceededException, UnknownObjectException, Auth

from .plugin import Plugin

if TYPE_CHECKING:
    from github.GitRelease import GitRelease
    from src.spp.types import SppPlugin


class GitPlugin(Plugin):
    """
    :metadata: структура плагина, получаемая от БД

    :_payload: объект нагрузки. Вызывается перед запуском постобработки.
    :_config: конфигурация.

    """

    def __init__(self, meta: SppPlugin):
        super().__init__(meta)

        self._payload: Callable = None

        self.REPOSITORY_ROOT_CATALOG_NAME: str | None = None
        self.PAYLOAD_FILENAME: str | None = None
        self.PAYLOAD_REPO_FILENAME: str | None = None  # Имя файла парсера в репозитории
        self.zip_repository: zipfile.ZipFile | None = None

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

    @property
    def payload(self) -> Callable | Exception:
        """
        Свойство, которое возвращает payload класс плагина
        :return:
        """
        if self._payload is None:
            self._payload = self._payload_python_class_from_file(
                self._path_for_filename(
                    self.config.payload.file, True
                )
            )

        return self._payload

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

    # Нужно обдумать метод загрузки и использования файлов из плагина
    def _zip_latest_release(self) -> zipfile.ZipFile | Exception:
        """
        Возвращает zip архив последнего релиза плагина
        :return:
        :rtype:
        """
        if not self.latest_release:
            self._log.exception('Plugin repository does not contain a release')
            raise UnknownObjectException(f'{str(self.latest_release)} не загружен')
        zip_bytes = requests.get(self.latest_release.zipball_url).content
        return zipfile.ZipFile(io.BytesIO(zip_bytes))

    def _extract_file_from_zip(self, filename: str, repository_filename: str):
        assert isinstance(self.PLUGIN_CATALOG_NAME, str)
        assert isinstance(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, str)

        with open(filename, 'wb') as ext_file:
            ext_file.write(self.zip_repository.read(repository_filename))

    def _payload_python_class_from_file(self, path: str) -> Callable:
        spec = importlib.util.spec_from_file_location("SPP.spp_plugin." + self.config.payload.file, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_payload = module.__dict__.__getitem__(self.config.payload.class_name)
        payload_class = plugin_payload
        return payload_class

    def _fill_plugin_const(self):
        """
        Чтобы получить PLUGIN_CATALOG_NAME, нужно найти в списке имя, принадлежащее директории,
         в котором бы был только один символ `/`
        Example:
                                                           {Вложенная папка}
            [no] CuberHuber-NSPK-DI-SPP-plugin-nist-092ba29/spp/rep/

            [yes] CuberHuber-NSPK-DI-SPP-plugin-nist-092ba29/
        """
        for name in self.zip_repository.namelist():
            if name.endswith('/') and name.count('/') == 1:
                self.REPOSITORY_ROOT_CATALOG_NAME = name
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
        Нужно реализовать валидацию плагина
        """
        return

    def _git_last_release(self) -> GitRelease:
        _release: GitRelease | None = None
        auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
        print(self.metadata.repository)
        with Github(auth=auth) as g:
            repository = g.get_repo(self.metadata.repository)
            _release = repository.get_latest_release()
        return _release

    def __eq__(self, other):
        if isinstance(other, GitPlugin):
            return self.metadata == other.metadata
        return False

    def __del__(self):
        # Delete documents
        # Нужно подумать, стоит ли хранить прошлые версии !!
        # plugin_dir = os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)
        # shutil.rmtree(plugin_dir, ignore_errors=True)
        ...
