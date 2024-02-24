from __future__ import annotations

import io
import datetime
import io
import os
from ftplib import FTP, Error
from hashlib import sha224
from typing import BinaryIO
import logging
from functools import wraps
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, BinaryIO

if TYPE_CHECKING:
    from src.spp.brokers.repository.data.abc_data_repository import AbcDataRepository
    from src.spp.plugin.abc_plugin import AbcPlugin
    from src.spp.types import SppTask, SPP_document, SppRefer


class FtpRepository(AbcDataRepository):
    """
    Репозиторий FTP-сервера
    """

    def __init__(self, ref: SppRefer):
        self._reference = ref
        self._log = logging.getLogger(self.__class__.__name__)

        self.PASSV_ADDR: str = os.environ.get('FS_HOST')
        self.FTP_USER: str = os.environ.get('FS_FTP_USER')
        self.FTP_PASS: str = os.environ.get('FS_FTP_PASS')
        self.WORK_DIR: str = os.environ.get('FS_WORK_DIR')
        self.BLOCKSIZE: int = int(os.environ.get('FS_BLOCKSIZE'))
        pass

    def file(self, document: SPP_document) -> io.BytesIO:
        """
        Возвращает байтовое представление документа, если он существует, из FTP-сервера
        :param document:
        :return:
        """

        session = self._ref_dir(self._work_dir(self._session()))

        filename = self._filename(document)

        if not self._exists(session, filename):
            raise FileExistsError(f'{filename} is not exists. Call method FtpRepository.save(document, data)')

        try:
            _bytes_stream = io.BytesIO()
            session.retrbinary(f"RETR {filename}", _bytes_stream.write)
            _bytes_stream.seek(0, 0)
            session.close()
            return _bytes_stream
        except Error as e:
            self._log.error(e)
            raise e
        except Exception as e:
            # Нужна ошибка файла в файловом сервере
            self._log.error(e)
            raise e

    def rename(self, document: SPP_document, new_filename: str) -> str | Exception:
        raise NotImplemented

    def delete(self, document: SPP_document) -> io.BytesIO:
        raise NotImplemented

    def save(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Сохраняет документ, если он существует, в FTP-сервере
        :param document:
        :param data:
        :return:
        """

        session = self._ref_dir(self._work_dir(self._session()))

        binaryfile = io.BytesIO(data) if isinstance(data, bytes) else data

        filename = self._filename(document)

        if self._exists(session, filename):
            raise FileExistsError(f'{filename} already exists. Call method FtpRepository.update(document, data)')

        try:
            session.storbinary("STOR " + filename, binaryfile, self.BLOCKSIZE)
            storage_link = f'{session.pwd()}/{filename}'
            session.close()
        except Error as e:
            self._log.error(e)
            raise e
        except Exception as e:
            # Нужна ошибка файла в файловом сервере
            self._log.error(e)
            raise e

        return storage_link

    def update(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Обновляет документ, если он существует, в FTP-сервере
        :param document:
        :param data:
        :return:
        """

        session = self._ref_dir(self._work_dir(self._session()))

        binaryfile = io.BytesIO(data) if isinstance(data, bytes) else data

        filename = self._filename(document)

        if not self._exists(session, filename):
            raise FileExistsError(f'{filename} is not exists. Call method FtpRepository.save(document, data)')

        try:
            session.storbinary("STOR " + filename, binaryfile, self.BLOCKSIZE)
            storage_link = f'{session.pwd()}/{filename}'
            session.close()
        except Error as e:
            self._log.error(e)
            raise e
        except Exception as e:
            # Нужна ошибка файла в файловом сервере
            self._log.error(e)
            raise e

        return storage_link

    def _session(self) -> FTP:
        try:
            ftp = FTP(self.PASSV_ADDR)
            self._log.info(f'FTP connecting to {ftp.login(self.FTP_USER, self.FTP_PASS)}')
        except ConnectionRefusedError as e:
            # Ошибка соединения
            self._log.error(f'FTP missing connection with error {e}')
            raise e
        except Exception as e:
            # Нужно сделать так, чтобы ошибка подключения
            self._log.error(f'FTP error {e}')
            raise e

        return ftp

    def _ref_dir(self, session: FTP) -> FTP:
        if not self._exists(session, self._reference.name):
            session.mkd(self._reference.name)

        cwd = session.cwd(self._reference.name)
        self._log.debug(f'Refer directory: {cwd}')
        return session

    def _work_dir(self, session: FTP) -> FTP:
        if not isinstance(self._reference.type, str):
            raise ValueError('SppRefer type missing')

        dir_name: str = f'{self.WORK_DIR}/{self._reference.type}'
        if not self._exists(session, dir_name):
            session.mkd(dir_name)

        cwd = session.cwd(dir_name)
        self._log.debug(f'Working directory: {cwd}')
        return session

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
