from selenium import webdriver


class WebDriver:

    def __new__(cls, *args, **kwargs) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()

        # Параметр для того, чтобы браузер не открывался.
        # options.add_argument('headless')

        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")

        return webdriver.Chrome(options)
