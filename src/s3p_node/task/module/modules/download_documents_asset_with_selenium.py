import datetime
import os
import time
from pathlib import Path

from s3p_sdk.types import S3PDocument
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

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
        super().__init__(bus, {
            'available_field': None,
            'cookie_selector': None,
            'temp_extensions': ('.crdownload', '.part'),
            'timeout': 30,
            'interval': 1
        })
        self.download()

    def download(self):
        with WebInstallerDriver(str(self.bus.temporary_directory)) as driver:
            for document in self.bus.documents.data:
                # available_field говорит о том, можно ли скачивать материал или нет
                assert document.other.get(self.config.get('available_field')) is not None
                if bool(document.other.get(self.config.get('available_field'))):
                    tempfilename = self._downloaded_filename(driver, document, self.bus.temporary_directory)
                    self._rename(self.bus.temporary_directory / tempfilename, document)
                    document.loaded = datetime.datetime.now()
                    self.logger.info(f'Document {document} asset downloaded')

    def _downloaded_filename(self, driver: webdriver.WebDriver, document: S3PDocument, folder: Path) -> str:
        initial_files = set(os.listdir(str(folder)))
        self.logger.debug("Initial directory contents:", initial_files)

        self._init_access(driver, document.link)
        start_time = time.time()
        while True:
            current_files = set(os.listdir(str(folder)))
            new_files = current_files - initial_files

            # Check for temporary and completed files
            temp_files = [f for f in new_files if f.endswith(self.config.get('temp_extensions'))]
            completed_files = [f for f in new_files if not f.endswith(self.config.get('temp_extensions'))]

            if not temp_files:
                if len(completed_files) > 0:
                    downloaded_file = self._largest_file(folder, completed_files)
                    self.logger.debug("Post-download directory contents:", current_files)
                    return downloaded_file

            if time.time() - start_time > self.config.get('timeout'):
                raise TimeoutError(
                    f"Download time out. Temp files: {temp_files}, Completed files: {completed_files}"
                )

            time.sleep(self.config.get('interval'))

    def _largest_file(self, folder: Path, filenames: list[str]) -> str:
        max_file = None
        max_size = 0
        for file in filenames:
            st_size = (folder / file).stat().st_size
            if st_size > max_size:
                max_size = st_size
                max_file = file
        return max_file

    def _rename(self, path: Path, document: S3PDocument):
        os.rename(str(path), str(path.parent / document.hash.hex()))

    def _init_access(self, driver, uri: str):
        driver.get(uri)
        if selector := self.config.get('cookie_selector'):
            self._agree_cookie_pass(driver, selector)
            time.sleep(2)
        time.sleep(1)

    def _agree_cookie_pass(self, driver: webdriver.WebDriver, cookie: str):
        try:
            cookie_button = driver.find_element(By.CSS_SELECTOR, cookie)
            if WebDriverWait(driver, 5).until(ec.element_to_be_clickable(cookie_button)):
                cookie_button.click()
                self.logger.debug(F"Parser pass cookie modal on page: {driver.current_url}")
        except NoSuchElementException as e:
            self.logger.debug(f'modal agree not found on page: {driver.current_url}')
