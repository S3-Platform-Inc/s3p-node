from dataclasses import dataclass
from typing import TYPE_CHECKING

from src.s3p_node.plugin.config.schemes.constant import ConstantObject
from src.s3p_node.plugin.config.schemes.module import Module
from src.s3p_node.plugin.config.schemes.file import FileObject

if TYPE_CHECKING:
    from . import ConstantObject, Module, FileObject


@dataclass
class EntryObject:
    """
    Объект, который подается в класс нагрузки
    """
    key: str
    value: FileObject | Module | ConstantObject
