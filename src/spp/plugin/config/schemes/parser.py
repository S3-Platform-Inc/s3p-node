from dataclasses import dataclass


@dataclass
class Parser:
    """
    :Parser: optional
        - Уникальное имя источника
        - Имя файла парсера
        - Имя класса парсера и точки входа
        - доп методы: optional
    """
    file_name: str
    class_name: str
    entry_point: str
    entry_keywords: tuple | None
    additional_methods: tuple | None
