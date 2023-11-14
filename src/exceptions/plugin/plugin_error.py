from logging import Logger


class PluginNotFoundError(FileNotFoundError):
    """
    ОШибка используется если не найден какой-то файл плагина.
    """

    def __init__(self, plugin_src: str, file: str = None, logger: Logger = None, git: bool = None):
        src_text = f"git" if git else "path"

        if file:
            message = f"The SPP cannot find the {file} of the plugin at the {src_text} specified {plugin_src}"
        else:
            message = f"The SPP cannot find the plugin at the {src_text} specified {plugin_src}"
        super().__init__(message)

        if logger:
            logger.error(message)
        ...
