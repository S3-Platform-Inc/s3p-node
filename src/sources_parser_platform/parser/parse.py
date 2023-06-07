import datetime
from typing import List

import pandas
from selenium import webdriver

from sources_parser_platform.parser.content_document import Content_Document
from sources_parser_platform.parser.source.pci import PCI


class Parse:
    """

    """
    HOST = 'https://www.pcisecuritystandards.org/document_library/'

    def __init__(self):
        pci_content = PCI(self.driver).content('', '')
        self._save_dataframe(self.content_documents_to_dataframe(pci_content))

    @property
    def driver(self) -> webdriver.Chrome:
        """

        :return:
        :rtype:
        """
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # OR options.add_argument("--disable-gpu")

        return webdriver.Chrome('chromedriver', chrome_options=options)

    def content_documents_to_dataframe(self, content: List[Content_Document]) -> pandas.DataFrame:
        """

        :param content:
        :type content:
        :return:
        :rtype:
        """
        pd_dataset = pandas.DataFrame(vars(row) for row in content)
        return pd_dataset

    def _save_dataframe(self, dataframe: pandas.DataFrame, name: str = 'dataset_content_documents_',
                        index: bool = False):
        # починить формат времени для сохранения файла
        dataframe.to_csv(name + str(datetime.datetime.now()), index=index)

    def _load_dataframe(self, name: str) -> pandas.DataFrame:
        """
        Загрузка датафрейма из файла
        :param name:
        :return:
        """
        return pandas.read_csv(name)

    def new_changes(self, old_dataframe: pandas.DataFrame, new_dataframe: pandas.DataFrame):
        """
        Возвращает список новых документов, которые потом нужно будет скачать
        :param old_dataframe: старая таблица с документами
        :type old_dataframe: pandas.DataFrame
        :param new_dataframe: новая таблица с документами
        :type new_dataframe: pandas.DataFrame
        :return:
        """
        ...

    def _save_buffer_content(self, name, content):
        ...
