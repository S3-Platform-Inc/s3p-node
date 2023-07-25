from logging import Logger


class PluginNotFoundError(FileNotFoundError):
    """
    ОШибка используется если не найден какой-то файл плагина.
    """

    def __init__(self, plugin_path: str, file: str = None, logger: Logger = None):
        if file:
            message = f"The system cannot find the {file} of the plugin at the path specified {plugin_path}"
        else:
            message = f"The system cannot find the plugin at the path specified {plugin_path}"
        super().__init__(message)

        if logger:
            logger.error(message)
        ...
