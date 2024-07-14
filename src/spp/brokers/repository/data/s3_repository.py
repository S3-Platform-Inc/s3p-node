from __future__ import annotations

import io
import logging
import os
from typing import TYPE_CHECKING, BinaryIO

import boto3

if TYPE_CHECKING:
    from src.spp.brokers.repository.data.abc_data_repository import AbcDataRepository
    from src.spp.types import SPP_document, SppRefer


class S3Repository(AbcDataRepository):
    """
    Репозиторий FTP-сервера
    """

    def __init__(self, ref: SppRefer):
        self._reference = ref
        self._log = logging.getLogger(self.__class__.__name__)

        print(self._client(self._session()).list_objects())

    def file(self, document: SPP_document) -> io.BytesIO:
        """
        Возвращает байтовое представление документа, если он существует, из FTP-сервера
        :param document:
        :return:
        """
        raise NotImplemented

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
        raise NotImplemented

    def update(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Обновляет документ, если он существует, в FTP-сервере
        :param document:
        :param data:
        :return:
        """
        raise NotImplemented

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

    @staticmethod
    def _filename(document: SPP_document):
        if document.local_link:
            name = document.local_link
        else:
            name = document.title + '_' + document.web_link + '_' + str(document.pub_date.timestamp())

        return name

    @staticmethod
    def _exists() -> bool:
        raise NotImplemented


if __name__ == '__main__':
    s3 = S3Repository(SppRefer(1, 'src', None, None))
