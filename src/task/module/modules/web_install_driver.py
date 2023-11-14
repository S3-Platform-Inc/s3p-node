import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)


class WebInstallerDriver:
    """
    Класс - рудимент.

    Не попадает под классификацию модулей, но пока находится тут.

    Настраивает и возвращает драйвер Selenium для скачивания файлов с противных источников (Nasty source)

    :Nasty source
    """

    def __new__(cls, dir_path: str, *args, **kwargs) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920x1080')

        options.add_argument('--no-sandbox')
        options.add_argument("--disable-gpu")
        # options.add_argument('headless')
        # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        options.add_argument("--start-maximized")  # open Browser in maximized mode
        options.add_argument('--disable-dev-shm-usage')
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)

        os.environ['WDM_LOG'] = str(logging.NOTSET)

        chrome_prefs = {
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "download.open_pdf_in_system_reader": False,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": dir_path,
        }
        # options.add_extension('Adblock-Plus_v1.4.1.crx')
        # options.add_argument(r'--user-data-dir=C:\Users\Roman\AppData\Local\Google\Chrome\User Data')
        options.add_experimental_option("prefs", chrome_prefs)
        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager(path=r'C:\Users\Roman\Desktop\.Drivers').install(),
            ),
            options=options,
        )
        return driver
