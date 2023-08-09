"""
Поток № (6) шины

Объект сущности потока шины SPP, хранящий брокер для работы с локальным хранилищем
"""
import io
from datetime import datetime
from typing import BinaryIO

from src.sources_parser_platform.brokers.ls_broker import SPP_temp_broker
from src.sources_parser_platform.types import SPP_source, SPP_document
from .. import Flow


class SPP_FE_local_storage(Flow):
    _local_broker: SPP_temp_broker

    def __init__(self, source: SPP_source, path: str):
        super().__init__()

        self._local_broker = SPP_temp_broker(source, path)

    @property
    def full_source_storage_path(self) -> str:
        """
        Абсолютный путь до каталога, привязанному к определенному источнику в локальном хранилище
        :return: абсолютный путь
        :rtype: str
        """
        return self._local_broker.source_dir

    def soft_save_current_file(self, document: SPP_document, filename: str):
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

    def file(self, document: SPP_document) -> BinaryIO:
        """
        Возвращает Bytes-like объект, представляющий бинарное представление файла, связанного с документом
        :param document: объект документа
        :type document: SPP_document
        :return: файл, связанный с документом в локальном хранилище
        :rtype: BinaryIO
        """
        return self._local_broker.file(document)

    def upload_file(self, document: SPP_document, data: bytes | io.BytesIO) -> bool | tuple[str, datetime]:
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
