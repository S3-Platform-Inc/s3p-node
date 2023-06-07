from selenium import webdriver


class WebDriver:

    def __new__(cls, *args, **kwargs) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # OR options.add_argument("--disable-gpu")

        return webdriver.Chrome('chromedriver', chrome_options=options)
