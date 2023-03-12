from dataclasses import dataclass


@dataclass
class Content_Document:
    title: str          # Заголовок
    pub_date: str       # Дата публикации
    abstract: str       # Пока пустое поле
    web_link: str       # Ссылка на веб-страницу, где можно получить (или прочитать) содержимое Документа
    local_link: str     # Локальная ссылка на загруженный файл с содержимым документа
    load_date: str      # Дата загрузки документа
    add_data: str       # Пока пустое поле
    category: str       # Категория материала
    sub_category: str   # Подкатегория материала
    version: str        # Версия документа
    source_name: str    #


class Document:

    def __init__(self, metadata: Content_Document):

        self.metadata = metadata
        ...

    def download(self):
        ...