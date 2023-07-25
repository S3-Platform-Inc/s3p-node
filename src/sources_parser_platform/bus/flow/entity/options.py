"""
Поток № (1) шины

Объект сущности потока шины SPP, содержащий все настройки для модулей задачи
"""
from ..flow import Flow


class SPP_FE_options(Flow):
    _options: dict[str, list]

    def __init__(self, module_options: list[tuple]):
        super().__init__()

        self._options = {name: params for name, params in module_options}
        ...

    def options(self, module_name) -> list:
        """
        Возвращает параметры по названию модуля
        :param module_name:
        :type module_name:
        :return:
        :rtype:
        """
        return self._options.get(module_name, [])
