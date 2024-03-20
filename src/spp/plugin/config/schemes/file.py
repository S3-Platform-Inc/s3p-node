from dataclasses import dataclass


@dataclass
class FileObject:
    """
    Объект, представляющий файл плагина
    """
    name: str
