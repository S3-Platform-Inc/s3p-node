import sys
from typing import Callable

from .modules import \
    DownloadDocumentsWithDB, \
    FilterOnlyNewDocumentWithDB, \
    WebDriver, \
    DownloadDocumentsWithParserMethods, \
    DownloadDocumentsThroughSeleniumTemp, \
    WebInstallerDriver, \
    ExtractTextFromFile, \
    UploadDocumentToDB, \
    TimezoneSafeControl

__all__ = [
    "get_module_by_name",
    "DownloadDocumentsWithDB",
    "FilterOnlyNewDocumentWithDB",
    "WebDriver",
    "DownloadDocumentsWithParserMethods",
    "DownloadDocumentsThroughSeleniumTemp",
    "WebInstallerDriver",
    "ExtractTextFromFile",
    "UploadDocumentToDB",
    "TimezoneSafeControl",
]


def get_module_by_name(modulename: str) -> Callable:
    """

    :rtype: object
    """
    # Добавить обработку исключений
    if modulename in __all__:
        return getattr(sys.modules[__name__], modulename)
    raise NotImplemented
