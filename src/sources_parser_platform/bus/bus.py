"""

"""
from src.sources_parser_platform.types import SPP_document
from .flow.entity import SPP_FE_options, SPP_FE_documents, SPP_FE_source, SPP_FE_database, SPP_FE_fileserver


class Bus:
    """

    """

    _options: SPP_FE_options
    _documents: SPP_FE_documents
    _source: SPP_FE_source
    _database: SPP_FE_database
    _fileserver: SPP_FE_fileserver

    def __init__(self, option, documents, source, database, fileserver):
        self._options = option
        self._documents = documents
        self._source = source
        self._database = database
        self._fileserver = fileserver

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
