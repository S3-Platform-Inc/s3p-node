"""

"""
from src.sources_parser_platform.types import SPP_document
from .flow.entity import \
    SPP_FE_options, \
    SPP_FE_documents, \
    SPP_FE_source, \
    SPP_FE_database, \
    SPP_FE_fileserver, \
    SPP_FE_local_storage


class Bus:
    """

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

    @property
    def options(self) -> SPP_FE_options:
        """

        :return:
        :rtype:
        """
        return self._options

    @property
    def documents(self) -> SPP_FE_documents:
        """

        :return:
        :rtype:
        """
        return self._documents

    @documents.setter
    def documents(self, doc: list[SPP_document]):
        self._documents = SPP_FE_documents(doc)

    @property
    def source(self) -> SPP_FE_source:
        """

        :return:
        :rtype:
        """
        return self._source

    @property
    def database(self) -> SPP_FE_database:
        """

        :return:
        :rtype:
        """
        return self._database

    @property
    def fileserver(self) -> SPP_FE_fileserver:
        return self._fileserver

    @property
    def local_storage(self) -> SPP_FE_local_storage:
        return self._local_storage

    def entity(self, key: str):
        if key in self._other:
            return self._other.get(key)
        else:
            # Искомого модуля нет
            raise NotImplemented
