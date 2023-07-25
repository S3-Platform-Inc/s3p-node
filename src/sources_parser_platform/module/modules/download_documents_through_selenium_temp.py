import io
import os
from functools import lru_cache

from sources_parser_platform.types import SPP_document
from src.sources_parser_platform.bus import Bus
from src.sources_parser_platform.module.spp_module import SPP_module
from .web_install_driver import WebInstallerDriver


class DownloadDocumentsThroughSeleniumTemp(SPP_module):
    """
    Модуль для скачивания документов, используя метод парсера для скачивания документа в локальное хранилище,
    с последующим переименованием и загрузкой в файловый сервер.

    DRAFT: Это тестовый модуль.
    """

    MAX_TRY = 5
    ENTITY_METHOD_NAME = 's_download'

    def __init__(self, bus: Bus):
        super().__init__(bus)
        self.download()

    def download(self):
        for doc in self.bus.documents.data:
            self._safe_download(doc)
            self._upload_to_fileserver(doc)
            ...
        ...

    def _safe_download(self, doc: SPP_document):
        d_filename = self._driver_download(doc.web_link)
        self.bus.local_storage.soft_save_current_file(doc, d_filename)
        ...

    def _upload_to_fileserver(self, doc: SPP_document):
        file_data = self.bus.local_storage.file(doc)
        with file_data as f:
            res = self.bus.fileserver.upload_file(doc, f)
            if res:
                local_link, load_date = res
                self.bus.documents.update(
                    doc,
                    SPP_document(
                        doc_id=doc.doc_id,
                        title=doc.title,
                        abstract=doc.abstract,
                        text=doc.text,
                        web_link=doc.web_link,
                        local_link=local_link,
                        other_data=doc.other_data,
                        pub_date=doc.pub_date,
                        load_date=load_date
                    ))
            else:
                # Нужно предусмотреть ошибки и сохранить в локальное хранилище
                raise NotImplemented

    def _driver_download(self, url: str) -> str:
        try:
            download_selenium_method = self.bus.entity(self.ENTITY_METHOD_NAME)
        except:
            # Нужно вставить ошибку получения несуществующей сущности
            raise NotImplemented

        ls_path = self.bus.local_storage.full_source_storage_path
        downloaded_filename = ""
        try:
            downloaded_filename = download_selenium_method(WebInstallerDriver(ls_path), ls_path, url)
            return downloaded_filename
        except Exception as e:
            print(e)
            # Ошибка запуска внешнего метода парсера
            raise NotImplemented
