"""
The Main Bus of S3P Node
"""
from __future__ import annotations

import logging
import pathlib
import tempfile
from typing import TYPE_CHECKING

from s3p_sdk.abstracts.abstract_repository import AbstaractRepository

from ..exceptions.bus.bus_entity_not_found_error import BusEntityNotFoundError

if TYPE_CHECKING:
    from s3p_sdk.types import S3PDocument
    from .flow.entity import \
        SppFeOptions, \
        SppFeDocuments, \
        SppFeSource, \
        SppFeDatabase, \
        SppFeFileserver, \
        SppFeLocalStorage


class Bus:
    """
    Класс главной шины SPP
    Шина содержит 6 главных потока и возможное множество дополнительных потоков

    Основные потоки:

    :options        : 
    :documents      :
    :source         :
    :database       :
    :fileserver     :
    :local storage  :

    """

    _options: SppFeOptions
    _documents: SppFeDocuments
    _source: SppFeSource
    _database: SppFeDatabase
    _fileserver: SppFeFileserver
    _local_storage: SppFeLocalStorage
    _temp_directory: tempfile.TemporaryDirectory
    _s3_repository: AbstaractRepository
    _other: dict

    def __init__(
            self,
            option: SppFeOptions,
            documents: SppFeDocuments,
            source: SppFeSource,
            database: SppFeDatabase,
            fileserver: SppFeFileserver,
            local_storage: SppFeLocalStorage,
            s3_repository: AbstaractRepository,
            **kwargs
    ):
        self._options = option
        self._documents = documents
        self._source = source
        self._database = database
        self._fileserver = fileserver
        self._local_storage = local_storage
        self._s3_repository = s3_repository
        self._other = {}

        for key in kwargs:
            self._other[key] = kwargs.get(key)

        # Temporary directory
        self._temp_directory = tempfile.TemporaryDirectory()

        self.log = logging.getLogger(self.__class__.__name__)

    @property
    def options(self) -> SppFeOptions:
        """
        Свойство предоставляет сущность настроек
        :return:
        :rtype: SppFeOptions
        """
        return self._options

    @property
    def documents(self) -> SppFeDocuments:
        """
        Свойство предоставляет сущность из потока documents
        :return: список объектов документов (SPP_documents)
        :rtype:
        """
        return self._documents

    @documents.setter
    def documents(self, docs: list[S3PDocument]):
        self._documents = SppFeDocuments(docs)

    @property
    def source(self) -> SppFeSource:
        """
        Свойство предоставляет сущность из потока source
        :return: объект источника (SPP_source)
        :rtype: SppFeSource
        """
        return self._source

    @property
    def database(self) -> SppFeDatabase:
        """
        Свойство предоставляет сущность из потока database
        :return: брокер базы данных
        :rtype: SppFeDatabase
        """
        return self._database

    @property
    def fileserver(self) -> SppFeFileserver:
        """
        Свойство предоставляет сущность из потока fileserver
        :return: брокер файлового сервера
        :rtype: SppFeFileserver
        """
        return self._fileserver

    @property
    def local_storage(self) -> SppFeLocalStorage:
        """
        Свойство предоставляет сущность из потока localstorage
        :return: брокер локального хранилища
        :rtype: SppFeLocalStorage
        """
        return self._local_storage

    @property
    def s3(self) -> AbstaractRepository:
        return self._s3_repository

    @property
    def temporary_directory(self) -> pathlib.Path:
        return pathlib.Path(self._temp_directory.name)

    @property
    def entity(self, key: str):
        """
        Метод возвращает дополнительную сущность по ключу
        :param key: Уникальное имя дополнительной сущности
        :type key: str
        :return: объект сущности
        :rtype: any
        """
        if key in self._other:
            return self._other.get(key)
        else:
            # Искомого модуля нет
            raise BusEntityNotFoundError(key, self.log)

    def __del__(self):
        self.cleanup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        self._temp_directory.cleanup()
