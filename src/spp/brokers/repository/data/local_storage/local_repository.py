from __future__ import annotations

import io
import logging
import os
from ftplib import FTP
from typing import TYPE_CHECKING, BinaryIO

from .control import ControlFile

if TYPE_CHECKING:
    from src.spp.brokers.repository.data.abc_data_repository import AbcDataRepository
    from src.spp.types import SPP_document, SppRefer


class LocalRepository(AbcDataRepository):
    """
    Репозиторий FTP-сервера
    """

    def __init__(self, ref: SppRefer):
        self._reference = ref
        self._log = logging.getLogger(self.__class__.__name__)

        self.BASE_PATH = os.environ.get('SPP_ABSOLUTE_PATH_TO_LOCAL_STORAGE')
        self.WORK_DIR: str = os.environ.get('LS_WORK_DIR')

        if not os.path.isdir(self._work_dir()):
            raise NotADirectoryError(f"{self._work_dir()} can't destinations")
        if not os.path.isdir(self._ref_dir()):
            os.mkdir(self._ref_dir())

        self._control = ControlFile(self._ref_dir())

    def file(self, document: SPP_document) -> BinaryIO:
        """
        Возвращает байтовое представление документа, если он существует, из локальном хранилище
        :param document:
        :return:
        """
        try:
            filename = self._control.filename(document)
        except KeyError as e:
            self._log.error(e)
            raise FileNotFoundError(f'Document {document} does not exist') from e

        return open(self._path(filename), 'rb')

    def link(self, document: SPP_document, filename: str) -> KeyError:
        if not os.path.isfile(self._path(filename)):
            self._log.error(f'File {filename} does not exist')
            raise FileNotFoundError(filename)

        self._control.add(document, filename)

    def rename(self, document: SPP_document, new_filename: str) -> Exception:
        try:
            filename = self._control.filename(document)
            os.rename(self._path(filename), self._path(new_filename))
            self._control.rename(document, new_filename)
        except Exception as e:
            self._log.error(e)
            raise e

    def delete(self, document: SPP_document) -> io.BytesIO:
        raise NotImplemented

    def save(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Сохраняет документ, если он существует, в локальном хранилище
        :param document:
        :param data:
        :return:
        """

        raise NotImplemented

    def update(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Обновляет документ, если он существует, в локальном хранилище
        :param document:
        :param data:
        :return:
        """

        raise NotImplemented

    def _ref_dir(self) -> str:
        return os.path.join(self._work_dir(), self._reference.name)

    def _work_dir(self) -> str:
        return os.path.join(self.BASE_PATH, self.WORK_DIR)

    def _path(self, filename: str) -> str:
        return os.path.join(self._ref_dir(), filename)

    @staticmethod
    def _filename(document: SPP_document):
        if document.local_link:
            name = document.local_link
        else:
            name = document.title + '_' + document.web_link + '_' + str(document.pub_date.timestamp())

        return name

    @staticmethod
    def _exists(session: FTP, name: str) -> bool:
        return name in list(session.nlst())
