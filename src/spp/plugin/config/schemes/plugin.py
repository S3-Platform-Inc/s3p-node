from dataclasses import dataclass


@dataclass
class Plugin:
    """
    :reference name: Уникальное имя связанного объекта, за который отвечает плагин (источник или модель)

    :plugin_type: Уникальный тип плагина (Parser | ML)

    :filenames: Кортеж файлов плагина, которые будут использоваться
    """
    reference_name: str
    type: str
    filenames: tuple[str]
