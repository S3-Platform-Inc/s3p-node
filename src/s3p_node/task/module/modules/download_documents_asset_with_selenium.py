import contextlib
import datetime
import os
import tempfile
from pathlib import Path

from s3p_sdk.types import S3PDocument
from selenium.webdriver.chrome import webdriver

from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from .web_install_driver import WebInstallerDriver


class DownloadDocumentsAssetWithSelenium(BaseModule):
    """
    Модуль для скачивания документов, используя метод парсера для скачивания документа в локальное хранилище,
    с последующим переименованием и загрузкой в файловый сервер.

    DRAFT: Это тестовый модуль.
    """

    MAX_TRY = 5

    def __init__(self, bus: Bus):
        super().__init__(bus)
        self.download()

    def download(self):
        with WebInstallerDriver(str(self.bus.temporary_directory)) as driver:
            for document in self.bus.documents.data:
                tempfilename = self.downloaded_filename(driver, document, self.bus.temporary_directory)
                self.rename(self.bus.temporary_directory / tempfilename, document)
                document.loaded = datetime.datetime.now()

    def downloaded_filename(self, driver: webdriver.WebDriver, document: S3PDocument, dir: Path) -> str:
        initial_files = set(os.listdir(dir))

        # some logic
        driver.get(document.link)

        files = set(os.listdir(dir))
        difference = files.difference(initial_files)
        if len(difference) != 1:
            # Something was terrable
            raise Exception(f'Something went wrong while downloading {dir} {difference}')

        filename = next(iter(difference))
        return filename

    def rename(self, path: Path, document: S3PDocument):
        path.rename(str(document.hash))
