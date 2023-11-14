import logging

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

LOGGER.setLevel(logging.WARNING)


class WebDriver:
    """
    Класс - рудимент.

    Не попадает под классификацию модулей, но пока находится тут.

    Настраивает и возвращает драйвер Selenium
    """

    def __new__(cls, *args, **kwargs) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()

        # Параметр для того, чтобы браузер не открывался.
        options.add_argument('headless')

        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        return webdriver.Chrome(options)
