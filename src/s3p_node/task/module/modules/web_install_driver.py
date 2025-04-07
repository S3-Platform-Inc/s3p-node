import logging
import os

from selenium import webdriver
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

        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--no-sandbox')  # Disable sandboxing, which is not suitable for Docker
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage, which can cause issues in Docker
        options.add_argument('--disable-gpu')  # Disable GPU acceleration, which is not necessary in a Docker container
        options.add_argument('--window-size=1920,1080')  # Set a default window size
        # options.add_argument('--remote-debugging-port=9222')  # Allow remote debugging
        options.add_argument('--disable-extensions')  # Disable extensions, which can cause issues
        options.add_argument('--disable-default-apps')  # Disable default apps, which can cause issues
        # options.add_argument('--proxy-server="direct://"')  # Disable proxy server
        # options.add_argument('--proxy-bypass-list=*')  # Bypass proxy for all destinations

        os.environ['WDM_LOG'] = str(logging.NOTSET)

        chrome_prefs = {
            "download.prompt_for_download": False,
            "plugins.always_open_pdf_externally": True,
            "download.open_pdf_in_system_reader": False,
            "profile.default_content_settings.popups": 0,
            "download.default_directory": dir_path,
        }
        options.add_experimental_option("prefs", chrome_prefs)

        driver = webdriver.Chrome(options=options)
        return driver
