import logging
import os

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule

LOGGER.setLevel(logging.WARNING)


class WebDriver(BaseModule):
    """
    Класс - рудимент.

    Не попадает под классификацию модулей, но пока находится тут.

    Настраивает и возвращает драйвер Selenium
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, {})
        self._is_remote = os.getenv('SELENIUM_WEBDRIVER_HOST') is not None

    def __call__(self, *args, **kwargs) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()

        options.add_argument('--no-sandbox')  # Disable sandboxing, which is not suitable for Docker
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--disable-dev-shm-usage')  # Disable shared memory usage, which can cause issues in Docker
        options.add_argument('--disable-gpu')  # Disable GPU acceleration, which is not necessary in a Docker container
        options.add_argument('--window-size=1920,1080')  # Set a default window size
        # options.add_argument('--remote-debugging-port=9222')  # Allow remote debugging
        options.add_argument('--disable-extensions')  # Disable extensions, which can cause issues
        options.add_argument('--disable-default-apps')  # Disable default apps, which can cause issues
        # options.add_argument('--proxy-server="direct://"')  # Disable proxy server
        # options.add_argument('--proxy-bypass-list=*')  # Bypass proxy for all destinations

        if self._is_remote:
            # remote selenium driver
            # Connect to the Selenium server running inside the Docker container
            driver = webdriver.Remote(os.getenv('SELENIUM_WEBDRIVER_HOST'), options=options)
        else:
            # locally selenium driver
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(40)
        return driver
