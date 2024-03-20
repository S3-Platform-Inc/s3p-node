"""
Поток № (5) шины

Объект сущности потока шины SPP, хранящий брокер для работы с файловым хранилищем
"""
from __future__ import annotations

import io
from datetime import datetime
from typing import BinaryIO, TYPE_CHECKING

from src.spp.brokers.ftpstorage import SppFileServerBroker
from .. import Flow

if TYPE_CHECKING:
    from src.spp.types import SppRefer, SPP_document


class SppFeFileserver(Flow):
    _file_broker: SppFileServerBroker

    def __init__(self, ref: SppRefer):
        super().__init__()

        self._file_broker = SppFileServerBroker(ref)
        ...

    def upload_file(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> bool | tuple[str, datetime]:
        """
        Метод загружает файл документа в FTP-сервер через брокер в сущности шины
        :param document:
        :type document:
        :param data:
        :type data:
        :return:
        :rtype:
        """
        res = self._file_broker.upload_document(document, data)
        if res:
            # файл сохранился
            return res, datetime.now()

        return False

    def file(self, document: SPP_document) -> io.BytesIO | BinaryIO:
        """
        Возвращает Bytes-like объект, представляющий бинарное представление файла, связанного с документом

        :exception: DRAFT

        :param document: объект документа
        :type document: SPP_document
        :return: файл, связанный с документом в файловом хранилище
        :rtype: BytesIO | BinaryIO
        """
        # Нужно помнить, что если что-то произойдет не так, то метод выкинет ошибку нахождения файла.
        res = self._file_broker.document(document)
        return res
