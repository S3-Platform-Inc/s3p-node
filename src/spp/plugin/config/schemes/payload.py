from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.spp.plugin.config.schemes.entry_object import EntryObject

if TYPE_CHECKING:
    from .entry_object import EntryObject


@dataclass
class Payload:
    """
    :file_name: имя файла .py с классом нагрузки.
    :class_name: имя класса нагрузки.
    :entry_point: имя метода, который нужно вызвать.
    :entry_keywords: кортеж элементов ключ-значение, которые нужно передать в конструктор класса.
    :additional_methods: дополнительные методы, которые нужно поместить в дополнительные потоки после инициализации класса
    """
    file_name: str
    class_name: str
    entry_point: str
    entry_keywords: tuple[EntryObject] | None
    additional_methods: tuple | None
