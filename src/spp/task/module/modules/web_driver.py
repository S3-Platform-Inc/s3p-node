import logging

from selenium import webdriver
from selenium.webdriver.remote.remote_connection import LOGGER

from src.spp.task.bus import Bus
from src.spp.task.module.base_module import BaseModule

LOGGER.setLevel(logging.WARNING)


class WebDriver(BaseModule):
    """
    Класс - рудимент.

    Не попадает под классификацию модулей, но пока находится тут.

    Настраивает и возвращает драйвер Selenium
    """

    def __init__(self, bus: Bus):
        super().__init__(bus, {})

    def __call__(self, *args, **kwargs) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()

        # Параметр для того, чтобы браузер не открывался.
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        return webdriver.Chrome(options)
