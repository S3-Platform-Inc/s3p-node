import io
from datetime import datetime
from typing import BinaryIO

from sources_parser_platform.brokers.fs_broker import SPP_file_server_broker
from sources_parser_platform.types import SPP_source, SPP_document
from .. import Flow


class SPP_FE_fileserver(Flow):
    _file_broker: SPP_file_server_broker

    def __init__(self, source: SPP_source):
        super().__init__()

        self._file_broker = SPP_file_server_broker(source)
        ...

    def upload_file(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> bool | tuple[str, datetime]:
        res = self._file_broker.upload_document(document, data)
        if res:
            # файл сохранился
            return res, datetime.now()

        return False

    def file(self, document: SPP_document) -> io.BytesIO | BinaryIO:
        # Нужно помнить, что если что-то произойдет не так, то метод выкинет ошибку нахождения файла.
        res = self._file_broker.document(document)
        return res
