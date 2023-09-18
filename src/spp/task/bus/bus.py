"""
Главная шина SPP
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..exceptions.bus.bus_entity_not_found_error import BusEntityNotFoundError

if TYPE_CHECKING:
    from spp.types import SPP_document
    from .flow.entity import \
        SPP_FE_options, \
        SPP_FE_documents, \
        SPP_FE_source, \
        SPP_FE_database, \
        SPP_FE_fileserver, \
        SPP_FE_local_storage


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

    _options: SPP_FE_options
    _documents: SPP_FE_documents
    _source: SPP_FE_source
    _database: SPP_FE_database
    _fileserver: SPP_FE_fileserver
    _local_storage: SPP_FE_local_storage
    _other: dict

    def __init__(
            self,
            option: SPP_FE_options,
            documents: SPP_FE_documents,
            source: SPP_FE_source,
            database: SPP_FE_database,
            fileserver: SPP_FE_fileserver,
            local_storage: SPP_FE_local_storage,
            **kwargs
    ):
        self._options = option
        self._documents = documents
        self._source = source
        self._database = database
        self._fileserver = fileserver
        self._local_storage = local_storage
        self._other = {}

        for key in kwargs:
            self._other[key] = kwargs.get(key)

        self.log = logging.getLogger(self.__class__.__name__)

    @property
    def options(self) -> SPP_FE_options:
        """
        Свойство предоставляет сущность настроек
        :return:
        :rtype: SPP_FE_options
        """
        return self._options

    @property
    def documents(self) -> SPP_FE_documents:
        """
        Свойство предоставляет сущность из потока documents
        :return: список объектов документов (SPP_documents)
        :rtype:
        """
        return self._documents

    @documents.setter
    def documents(self, docs: list[SPP_document]):
        self._documents = SPP_FE_documents(docs)

    @property
    def source(self) -> SPP_FE_source:
        """
        Свойство предоставляет сущность из потока source
        :return: объект источника (SPP_source)
        :rtype: SPP_FE_source
        """
        return self._source

    @property
    def database(self) -> SPP_FE_database:
        """
        Свойство предоставляет сущность из потока database
        :return: брокер базы данных
        :rtype: SPP_FE_database
        """
        return self._database

    @property
    def fileserver(self) -> SPP_FE_fileserver:
        """
        Свойство предоставляет сущность из потока fileserver
        :return: брокер файлового сервера
        :rtype: SPP_FE_fileserver
        """
        return self._fileserver

    @property
    def local_storage(self) -> SPP_FE_local_storage:
        """
        Свойство предоставляет сущность из потока localstorage
        :return: брокер локального хранилища
        :rtype: SPP_FE_local_storage
        """
        return self._local_storage

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
