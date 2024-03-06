import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.spp.task.bus import Bus


class BaseModule:
    """
    Базовый класс модуля

    :DEF_CONFIG: Конфигурация модуля по умолчанию, устанавливается модулями-наследниками.

    :config(): Свойство, которое возвращает настройки модуля;
    (подгружает настройки и перезаписывает стандартные настройки модуля) при необходимости;
    для работы требует передачу в реализации модуля DEF_CONFIG в конструктор BaseModule

    config - dict type. с Форматом Key: Value (Object)
    ! Warning - ключи конфигурации, которые были получены из шины, ОБЯЗАНЫ присутствовать в DEF_CONFIG.
    """
    DEF_CONFIG: dict

    def __init__(self, bus, def_config: dict = None):
        if def_config is None:
            def_config = {}
        self.bus = bus
        self._config: dict | None = None
        self._def_config: dict | None = def_config
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def config(self) -> dict:
        """
        Свойство, возвращающее настройки для модуля.
        Может быть использовано в реализации конкретного модуля
        :return: Module
        """
        assert self._def_config
        if self._config is None:
            try:
                config = self.bus.options.config(self.__class__.__name__).options
                if isinstance(config, dict):
                    self._config = self._def_config
                    self._config |= config
            except ModuleNotFoundError as e:
                self.logger.error(f'Bus not contained config for "{self.__class__.__name__}" module')
                return self._def_config
        # raise NameError(f'Bus not contained config for "{self.__class__.__name__}" module') from e

        return self._config
