"""
Тип данных для парсера и этапов обработки
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Content_Document:
    """
    Унифицированный тип данных, который используется при
    """

    title: str  # Заголовок
    pub_date: datetime  # Дата публикации
    abstract: str  # Пока пустое поле
    web_link: str  # Ссылка на веб-страницу, где можно получить (или прочитать) содержимое Документа
    local_link: str  # Локальная ссылка на загруженный файл с содержимым документа
    load_date: datetime  # Дата загрузки документа
    add_data: str  # Пока пустое поле
    category: str  # Категория материала
    sub_category: str  # Подкатегория материала
    version: str  # Версия документа
    source_name: str  # Уникальное название источника

    def __hash__(self):
        """
        Для проверки уникальности и новизны документа.

        :return:
        :rtype:
        """
        return hash((self.title, self.web_link, self.pub_date))
