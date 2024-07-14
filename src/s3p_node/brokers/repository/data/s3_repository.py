from __future__ import annotations

import io
import logging
import os
from typing import TYPE_CHECKING, BinaryIO

import boto3

if TYPE_CHECKING:
    from src.s3p_node.brokers.repository.data.abc_data_repository import AbcDataRepository
    from s3p_sdk.types import S3PDocument, S3PRefer


class S3Repository(AbcDataRepository):
    """
    Репозиторий FTP-сервера
    """

    def __init__(self, ref: S3PRefer):
        self._reference = ref
        self._log = logging.getLogger(self.__class__.__name__)

        print(self._client(self._session()).list_objects())

    def file(self, document: S3PDocument) -> io.BytesIO:
        """
        Возвращает байтовое представление документа, если он существует, из FTP-сервера
        :param document:
        :return:
        """
        raise NotImplemented

    def rename(self, document: S3PDocument, new_filename: str) -> str | Exception:
        raise NotImplemented

    def delete(self, document: S3PDocument) -> io.BytesIO:
        raise NotImplemented

    def save(self, document: S3PDocument, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Сохраняет документ, если он существует, в FTP-сервере
        :param document:
        :param data:
        :return:
        """
        raise NotImplemented

    def update(self, document: S3PDocument, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
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
    def _filename(document: S3PDocument):
        if document.storage:
            name = document.storage
        else:
            name = document.title + '_' + document.link + '_' + str(document.published.timestamp())

        return name

    @staticmethod
    def _exists() -> bool:
        raise NotImplemented


if __name__ == '__main__':
    s3 = S3Repository(S3PRefer(1, 'src', None, None))
