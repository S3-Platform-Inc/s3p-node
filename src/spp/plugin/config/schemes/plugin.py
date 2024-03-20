from dataclasses import dataclass


@dataclass
class Plugin:
    """
    :reference: Уникальное имя связанного объекта, за который отвечает плагин (источник или модель).

    :type: *Уникальный тип плагина (Parser | ML)

    :filenames: *Кортеж файлов плагина, которые будут использоваться

    :localstorage: Настройка локального хранилища: определяет как задача будет работать
    (отправлять только на файловый сервер или локально дублировать файлы
    """
    reference: str
    type: str
    filenames: tuple[str]
    localstorage: bool | None
