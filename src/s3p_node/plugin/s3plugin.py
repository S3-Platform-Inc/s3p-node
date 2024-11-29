"""
gitplugin.py
"""

from __future__ import annotations

import dataclasses
import importlib.util
import os
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Callable, TYPE_CHECKING

import boto3

from .plugin import Plugin

if TYPE_CHECKING:
    from s3p_sdk.types import S3PPlugin


@dataclasses.dataclass
class Manifest:
    version: str
    plugin_name: str


class S3Plugin(Plugin):
    """
    :metadata: структура плагина, получаемая от БД

    :_payload: объект нагрузки. Вызывается перед запуском постобработки.
    :_config: конфигурация.

    """

    def __init__(self, meta: S3PPlugin):
        super().__init__(meta)

        self._payload: Callable = None

        self.REPOSITORY_ROOT_CATALOG_NAME: str | None = None
        self.PAYLOAD_FILENAME: str | None = None
        self.PAYLOAD_REPO_FILENAME: str | None = None  # Имя файла парсера в репозитории
        self.zip_repository: zipfile.ZipFile | None = None
        self._manifest: Manifest | None = None

        try:
            self._fill_plugin_const()
            self.must_load_files()
        except Exception as e:
            self._log.exception('Plugin repository does not necessary structure')
            raise e
        else:
            self._verify()

    @property
    def manifest(self) -> Manifest:
        if self._manifest is None:
            self._must_load_manifest()
        return self._manifest

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

    # def file(self, filename: str) -> BinaryIO | io.BytesIO | Exception:
    #     """
    #     Методы возвращает файл плагина по его мени
    #     """
    #     if isinstance(filename, str):
    #         _path = self._path_for_filename(filename, True)
    #         with open(_path, 'rb') as file:
    #             return io.BytesIO(file.read())
    #     else:
    #         raise TypeError(f'filename must be of str type')

    # Нужно обдумать метод загрузки и использования файлов из плагина
    # def _zip_latest_release(self) -> zipfile.ZipFile | Exception:
    #     """
    #     Возвращает zip архив последнего релиза плагина
    #     :return:
    #     :rtype:
    #     """
    #     if not self.latest_release:
    #         self._log.exception('Plugin repository does not contain a release')
    #         raise UnknownObjectException(f'{str(self.latest_release)} не загружен')
    #     zip_bytes = requests.get(self.latest_release.zipball_url).content
    #     return zipfile.ZipFile(io.BytesIO(zip_bytes))

    # def _extract_file_from_zip(self, filename: str, repository_filename: str):
    #     assert isinstance(self.PLUGIN_CATALOG_NAME, str)
    #     assert isinstance(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, str)
    #
    #     with open(filename, 'wb') as ext_file:
    #         ext_file.write(self.zip_repository.read(repository_filename))

    def _payload_python_class_from_file(self, path: str) -> Callable:
        spec = importlib.util.spec_from_file_location(
            f"S3P.s3p_plugin.{self.config.payload.file}", path)
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
        self.REPOSITORY_ROOT_CATALOG_NAME = self.manifest.plugin_name

    # def _extract_plugin_files(self):
    #     assert isinstance(self.REPOSITORY_ROOT_CATALOG_NAME, str)
    #
    #     if not os.path.isdir(os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)):
    #         os.mkdir(os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME))
    #
    #     for filename in self.config.plugin.filenames:
    #         repository_filename = os.path.join(self.REPOSITORY_ROOT_CATALOG_NAME, filename)
    #         self._extract_file_from_zip(self._path_for_filename(filename, mkdir=True), repository_filename)

    def _verify(self):
        """
        Нужно реализовать валидацию плагина
        """
        return

    # def _git_last_release(self) -> GitRelease:
    #     _release: GitRelease | None = None
    #     auth = Auth.Token(str(os.getenv("GITHUB_TOKEN")))
    #     print(self.metadata.repository)
    #     with Github(auth=auth) as g:
    #         repository = g.get_repo(self.metadata.repository)
    #         _release = repository.get_latest_release()
    #     return _release

    def _session(self) -> boto3.Session:
        return boto3.Session(
            aws_access_key_id=os.environ.get('S3_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('S3_SECRET_ACCESS_KEY'),
        )

    def _client(self, session: boto3.Session):
        return session.client(
            service_name='s3',
            region_name=os.environ.get('S3_REGION_NAME'),
            endpoint_url=os.environ.get('S3_ENDPOINT_URL')
        )

    def must_load_files(self):
        _pl_files_path = f'plugins/{self.metadata.repository}/src/{self.manifest.plugin_name}'

        if not os.path.isdir(os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)):
            os.mkdir(os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME))

        for filename in self.config.plugin.filenames:
            _f = self._must_load_object(_pl_files_path + '/' + filename)
            self._save_file(self._path_for_filename(filename, mkdir=True), _f)

    def _save_file(self, filename: str, body: bytes):
        assert isinstance(self.PLUGIN_CATALOG_NAME, str)
        assert isinstance(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, str)

        with open(filename, 'wb') as ext_file:
            ext_file.write(body)

    def _must_load_manifest(self) -> None:
        _plugin_path = f'plugins/{self.metadata.repository}'
        _xml_path = _plugin_path + '/plugin.xml'
        a = self._must_load_object(_xml_path)
        self._manifest = self._parse_manifest(a.decode())

    def _parse_manifest(self, payload: str) -> Manifest:
        ROOT_TAG: str = "project"
        PROJECT_NAME_TAG: str = "name"
        PROJECT_VERSION_TAG: str = "version"
        try:
            tree = ET.ElementTree(ET.fromstring(payload))
            assert tree.getroot().tag == ROOT_TAG, \
                f"Не найден тег `{ROOT_TAG}` в корне plugin.xml"
            assert tree.getroot().attrib.get(PROJECT_NAME_TAG), \
                f"Не найдено поле `{PROJECT_NAME_TAG}` в теги `{ROOT_TAG}`"
            assert tree.getroot().find(PROJECT_VERSION_TAG).tag == PROJECT_VERSION_TAG, \
                f"Не найден тег `{PROJECT_VERSION_TAG}` в теги `{ROOT_TAG}`"

            return Manifest(
                version=str(tree.getroot().find(PROJECT_VERSION_TAG).text),
                plugin_name=tree.getroot().attrib.get('name')
            )
        except Exception as e:
            raise ValueError("S3P Plugin manifest file (plugin.xml) no exists or have some errors") from e

    def _must_load_object(self, path) -> bytes:
        _obj = self._client(
            self._session()
        ).get_object(
            Bucket=os.environ.get('S3_BUCKET_NAME'),
            Key=path
        )
        assert _obj
        return _obj.get('Body').read()

    def __del__(self):
        # Delete documents
        # Нужно подумать, стоит ли хранить прошлые версии !!
        # plugin_dir = os.path.join(self.BASE_PLUGIN_ARCHIVE_DIR_PATH, self.PLUGIN_CATALOG_NAME)
        # shutil.rmtree(plugin_dir, ignore_errors=True)
        ...


if __name__ == '__main__':
    meta = S3PPlugin(None, '', True, None, None, None)
    sp = S3Plugin(meta)

    print(sp.config)
