from dataclasses import dataclass
from .restrictionsobject import RestrictionsObject


@dataclass
class Plugin:
    """
    Класс, представляющий конфигурацию плагина.

    Attributes:
        reference (str): Уникальное имя связанного объекта, за который отвечает плагин (источник или модель).
        type (str): Уникальный тип плагина (Parser | ML).
        filenames (tuple[str]): Кортеж файлов плагина, которые будут использоваться.
        localstorage (bool | None): Настройка локального хранилища. Определяет, как задача будет работать
            (отправлять только на файловый сервер или локально дублировать файлы).
        restrictions (RestrictionsObject): Объект, содержащий ограничения для работы плагина.

    Этот класс используется для конфигурации плагина, определяя его основные характеристики,
    тип, используемые файлы, настройки хранения и ограничения.
    """
    reference: str
    type: str
    filenames: tuple[str]
    localstorage: bool | None
    restrictions: RestrictionsObject
