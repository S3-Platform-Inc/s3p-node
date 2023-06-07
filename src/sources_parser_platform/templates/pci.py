import time
from typing import List

from dateutil.parser import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait, Select

from sources_parser_platform.parser.content_document import Content_Document
from sources_parser_platform.parser.source.abc_source_documents import ABC_Source_Document


class PCI(ABC_Source_Document):
    # Типы документов на сайте
    _DOCUMENT_TYPES = (
        'All Document',
        'PCI DSS',
        'SAQ',
        'P2PE',
        'PTS',
        'Card Production',
        'MPoC',
        '3DS',
        'CPoC',
        'PIN',
        'SPoC',
        'TSP',
        'Software Security',
        'Programs and Certification',
        'Guidance Document',
        'Case Study',
    )
    HOST = 'https://www.pcisecuritystandards.org/document_library/'
    SOURCE_NAME = 'PCI'

    CATEGORY_CLASS_NAME = 'doc_library_category parent_category'
    SUB_CATEGORY_CLASS_NAME = 'doc_library_category category'
    DOCUMENTS_ROW_CLASS_NAME = 'document_row_container'

    DOCUMENT_TYPE = ''

    _content_document: List[Content_Document]

    def __init__(self, driver, document_type: str = 'All Document'):
        print(driver)
        print(document_type)
        assert document_type in self._DOCUMENT_TYPES
        self.DOCUMENT_TYPE = document_type
        self._content_document = []
        self.driver = driver

    def content(self, category_type: str = '', subcategory_type: str = '') -> List[Content_Document]:

        self._parse()
        return self._content_document

    def _parse(self):
        self.driver.set_page_load_timeout(40)
        self.driver.get(url=self.HOST)
        time.sleep(2)

        # прохождение панели с куками
        ccc_accept = self.driver.find_element(By.ID, 'ccc-notify-accept')
        if WebDriverWait(self.driver, 5).until(ec.element_to_be_clickable(ccc_accept)):
            ccc_accept.click()

        # Прокрутка до области с выбором типа документов
        WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.ID, 'results')))
        if WebDriverWait(self.driver, 2).until(
                ec.element_to_be_clickable(self.driver.find_element(By.ID, 'search_by_doc_Type'))):
            document_category = self.driver.find_element(By.ID, 'document_category')

            # Выбор всех документов
            select = Select(document_category)
            select.select_by_value('all_documents')

            # обработка всех документов
            current_category = ''
            current_sub_category = ''
            rows_container = self.driver.find_element(By.ID, 'tabcontent').find_elements(By.TAG_NAME, 'div')

            for row in rows_container:
                # Если в списке есть категория, она записывается в текущую категорию.
                # и Все следующие документы до новой категории, будут относить к этой категории
                if row.get_attribute('class') == self.CATEGORY_CLASS_NAME:
                    current_category = row.text
                # Аналогично категориям, только для субкатегорий
                elif row.get_attribute('class') == self.SUB_CATEGORY_CLASS_NAME:
                    current_sub_category = row.text
                #
                elif row.get_attribute('class') == self.DOCUMENTS_ROW_CLASS_NAME:

                    # Название документа
                    document_name = row.find_element(By.CLASS_NAME, 'document_name').text

                    # На сайте может быть элемент select для выбора версии документа или просто div с текстом версии
                    version_select_or_div = [el for el in row.find_elements(By.TAG_NAME, 'div') if
                                             'version_select' in el.get_attribute('id')]
                    document_version_and_pub_date = ''
                    if len(version_select_or_div) == 1:
                        try:
                            document_version_and_pub_date = Select(
                                version_select_or_div[0].find_element(By.TAG_NAME,
                                                                      'select')).first_selected_option.text
                        except:
                            document_version_and_pub_date = version_select_or_div[0].text

                    # Ссылка на документа
                    link_to_document = row.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    document_version, document_pub_date = self._get_version_and_date(document_version_and_pub_date)

                    self._content_document.append(Content_Document(
                        document_name,
                        document_pub_date,
                        '',
                        link_to_document,
                        '',
                        '',
                        '',
                        current_category,
                        current_sub_category,
                        document_version,
                        self.SOURCE_NAME,
                    ))
                    print(
                        f'[DATA]\t|\tcategory[{current_category}], sub_category[{current_sub_category}], '
                        f'document[{document_name}], version[{document_version_and_pub_date}], '
                        f'href[{link_to_document}]')

        time.sleep(5)
        self.driver.close()
        self.driver.quit()

    @staticmethod
    def _get_version_and_date(ctx: str):
        version_and_date = ctx.split(' - ')
        if len(version_and_date) == 2:
            return version_and_date[0], parse(version_and_date[1], fuzzy=True).isoformat()
        if len(version_and_date) == 1 and version_and_date[0].startswith('v'):
            return version_and_date[0], ''
        else:
            return '', parse(version_and_date[0], fuzzy=True).isoformat()
