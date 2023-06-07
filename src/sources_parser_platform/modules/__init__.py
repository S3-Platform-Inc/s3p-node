import sys

from .webdriver import WebDriver

__all__ = [
    "WebDriver",
    "get_module_by_name",
]


def get_module_by_name(modulename: str):
    # Добавить обработку исключений
    if modulename in __all__:
        return getattr(sys.modules[__name__], modulename)
    ...
