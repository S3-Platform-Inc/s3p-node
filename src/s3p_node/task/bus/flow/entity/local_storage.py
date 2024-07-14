"""
Поток № (6) шины

Объект сущности потока шины SPP, хранящий брокер для работы с локальным хранилищем
"""
from __future__ import annotations

import io
from datetime import datetime
from typing import BinaryIO, TYPE_CHECKING

from src.s3p_node.brokers.localstorage import SppTempBroker
from .. import Flow

if TYPE_CHECKING:
    from s3p_sdk.types import S3PRefer, S3PDocument


class SppFeLocalStorage(Flow):
    _local_broker: SppTempBroker

    def __init__(self, ref: S3PRefer, path: str):
        super().__init__()

        self._local_broker = SppTempBroker(ref, path)

    @property
    def full_source_storage_path(self) -> str:
        """
        Абсолютный путь до каталога, привязанному к определенному источнику в локальном хранилище
        :return: абсолютный путь
        :rtype: str
        """
        return self._local_broker.source_dir

    def soft_save_current_file(self, document: S3PDocument, filename: str):
        """
        Метод находит скачанный ранее файл по его имени, создает связь с документом,
        а затем переименовывает его выбранным способом
        :param document: объект документа
        :type document: SPP_document
        :param filename: имя файла скачанного файла
        :type filename: str
        """
        self._local_broker.link(document, filename)
        self._local_broker.rename(document)

    def file(self, document: S3PDocument) -> BinaryIO:
        """
        Возвращает Bytes-like объект, представляющий бинарное представление файла, связанного с документом
        :param document: объект документа
        :type document: SPP_document
        :return: файл, связанный с документом в локальном хранилище
        :rtype: BinaryIO
        """
        return self._local_broker.file(document)

    def upload_file(self, document: S3PDocument, data: bytes | io.BytesIO) -> bool | tuple[str, datetime]:
        """
        DRAFT
        :param document:
        :type document:
        :param data:
        :type data:
        :return:
        :rtype:
        """

        # Оставить для возможности загрузить байты в файл

        res = self._local_broker.upload_document(document, data)
        if res:
            # файл сохранился
            return res, datetime.now()

        return False
