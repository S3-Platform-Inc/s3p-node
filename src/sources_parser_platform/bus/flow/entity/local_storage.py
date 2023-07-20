import io
from datetime import datetime
from typing import BinaryIO

from sources_parser_platform.brokers.ls_broker import SPP_temp_broker
from sources_parser_platform.types import SPP_source, SPP_document
from .. import Flow


class SPP_FE_local_storage(Flow):
    _local_broker: SPP_temp_broker

    def __init__(self, source: SPP_source, path: str):
        super().__init__()

        self._local_broker = SPP_temp_broker(source, path)
        ...

    @property
    def full_source_storage_path(self) -> str:
        return self._local_broker.source_dir

    def soft_save_current_file(self, document: SPP_document, filename: str):
        self._local_broker.link(document, filename)
        self._local_broker.rename(document)
        ...

    def file(self, document: SPP_document) -> BinaryIO:
        return self._local_broker.file(document)

    def upload_file(self, document: SPP_document, data: bytes | io.BytesIO) -> bool | tuple[str, datetime]:
        # Оставить для возможности загрузить байты в файл

        res = self._local_broker.upload_document(document, data)
        if res:
            # файл сохранился
            return res, datetime.now()

        return False
