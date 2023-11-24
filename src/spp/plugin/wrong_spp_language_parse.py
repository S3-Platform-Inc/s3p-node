import logging

from spp.plugin.config import Config
from spp.plugin.config.schemes import Task, Parser, Module, Middleware


class WRONG_SPP_Language_Parse:
    """
    Временный парсер конфигурации
    """
    INSTRUCTIONS = (
        "PARSER",
        "FROM",
        "SET",
        "START",
        "ADD",
        "INIT",
        "RETURN",
        "SOURCE",
        "BUS_ADD",
    )
    __vars: dict

    source_name: str

    parser_filename: str
    parser_classname: str
    parser_method: str
    parser_init_keywords: list

    restart_interval: str

    bus_entities: list

    pipelines: list

    def __init__(self, src: str | list[str]):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.debug("SPPfile parser start")

        # Переопределяем свойства во избежание проблем с возможными ошибками или багами. ООП в Python ....
        self.__vars = {}
        self.parser_init_keywords = []
        self.restart_interval = None
        self.bus_entities = []
        self.pipelines = []

        self.__parse(self.__prepare_useful_commands(src))
        self.logger.debug("SPPfile parser finished")

    def config(self) -> Config:
        """
        Метод возвращает объект настроек
        :return:
        :rtype:
        """
        return Config(
            self.source_name,
            Task(  # DRAFT нет обработчика
                -1,
                self.restart_interval
            ),
            Middleware(
                tuple(self.pipelines),
                tuple(self.bus_entities)
            ),
            Parser(
                self.parser_filename,
                self.parser_classname,
                self.parser_method,
                tuple(self.parser_init_keywords),
                None
            )
        )

    def __prepare_useful_commands(self, text: str | list[str]) -> list[str]:
        useful_lines: list[str] = []
        lines: list[str] = []

        if isinstance(text, list):
            lines = [line.replace('\n', '') for line in text]
        elif isinstance(text, str):
            lines = [line for line in text.split('\n')]

        # Check lines
        # Выбирает те строки, в которых есть полезные команды из списка команд
        for line in lines:
            if any(line.startswith(instruction) for instruction in self.INSTRUCTIONS):
                useful_lines.append(line)

        return useful_lines

    def __parse(self, commands: list[str]):
        # ОСТОРОЖНО, ГОВНОКОД!!!!!

        # тут по хорошему организовать нормальную валидацию и обработку инструкций
        for cmd in commands:
            if cmd.startswith('PARSER'):
                self.parser_filename = cmd.split()[1]

                self.logger.debug(f"Set parser file : {self.parser_filename}")

            elif cmd.startswith('START'):
                classname, method = cmd.split()[1:]
                self.parser_classname = classname
                self.parser_method = method

                self.logger.debug(f"Set parser classname : {self.parser_classname}")
                self.logger.debug(f"Set parser class method : {self.parser_method}")

            elif cmd.startswith('SOURCE'):
                self.source_name = cmd.split()[1]

                self.logger.debug(f"Set unique source name is {self.source_name}")

            elif cmd.startswith('INIT'):
                keyword, module = cmd.split()[1:]
                self.parser_init_keywords.append((keyword, module))

                self.logger.debug(f"Set init parser parameter named {keyword} which represents {module}")

            elif cmd.startswith('SET'):
                keyword, *param = cmd.split()[1:]
                if keyword == "restart-interval":
                    self.restart_interval = ' '.join(param)
                    self.logger.debug(f"Set restart interval is {param}")

            elif cmd.startswith('ADD'):
                module, *params = cmd.split()[1:]

                _critical = bool(params and params[0].lower() == "critical")
                self.pipelines.append(Module(module, params, _critical))

                self.logger.debug(f"Add pipeline module named: {module}, with parameters: {params}")

            elif cmd.startswith('BUS_ADD'):
                module, *params = cmd.split()[1:]
                self.bus_entities.append((module, params))

                self.logger.debug(f"Add new bus flow named: {module}, with parameters: {params}")
