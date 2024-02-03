import logging
import re

from src.spp.plugin.config import Config
from src.spp.plugin.config.schemes import Task, Payload, Module, Middleware, Plugin, EntryObject


class WRONG_SPP_Language_Parse:
    """
    Временный парсер конфигурации
    """
    INSTRUCTIONS = (
        "TYPE",
        "PAYLOAD",
        "FROM",
        "SET",
        "ENTRY",
        "ADD",
        "INIT",
        "RETURN",
        "REF",
        "NEW_FLOW",
        "FILE",
    )
    __vars: dict
    __plugin_files: list

    reference_name: str | None
    plugin_type: str | None

    payload_filename: str | None
    payload_classname: str | None
    payload_method: str | None
    payload_init_keywords: list

    restart_interval: str | None
    logmod: str | None

    bus_entities: list
    pipelines: list

    def __init__(self, src: str | list[str]):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.debug("SPPfile parse start")

        # Переопределяем свойства во избежание проблем с возможными ошибками или багами. ООП в Python ....
        self.__vars = {}
        self.__plugin_files = []

        self.reference_name = None
        self.plugin_type = None

        self.payload_filename = None
        self.payload_classname = None
        self.payload_method = None
        self.payload_init_keywords = []

        self.restart_interval = None
        self.logmod = None

        self.bus_entities = []
        self.pipelines = []

        self.__parse(self.__prepare_useful_commands(src))
        self.logger.debug("SPPfile parse done")

    @property
    def config(self) -> Config:
        """
        Метод возвращает объект настроек
        :return:
        :rtype:
        """
        return Config(
            Plugin(
                reference_name=self.reference_name,
                type=self.plugin_type,
                filenames=tuple(self.__plugin_files)
            ),
            Task(  # DRAFT нет обработчика
                log_mode=-1,
                restart_interval=self.restart_interval
            ),
            Middleware(
                modules=tuple(self.pipelines),
                additional_bus_entities=tuple(self.bus_entities)
            ),
            Payload(
                file_name=self.payload_filename + '.py',
                class_name=self.payload_classname,
                entry_point=self.payload_method,
                entry_keywords=tuple(self.payload_init_keywords),
                additional_methods=None
            )
        )

    def __prepare_useful_commands(self, text: str | list[str]) -> list[str]:
        useful_lines: list[str] = []
        lines: list[str] = []

        if isinstance(text, list):
            lines = [line.replace('\n', '') for line in text]
        elif isinstance(text, str):
            lines = [line for line in text.split('\n')]

        # Шаблон для проверки и выделения первой инструкции и параметров
        # re_template = "^([_A-Z]+) ([\w\d\=\ \-\.\/]+[\w\d])$"


        # Check lines
        # Выбирает те строки, в которых есть полезные команды из списка команд
        for line in lines:
            if any(line.startswith(instruction) for instruction in self.INSTRUCTIONS):

                # Удаляет все пробелы и комменты после инструкции и параметров
                regex = r" *#.*"
                line = re.sub(regex, "", line, 0, re.MULTILINE)
                useful_lines.append(line)

        return useful_lines

    def __parse(self, commands: list[str]):
        # ОСТОРОЖНО, ГОВНОКОД!!!!!

        # тут по хорошему организовать нормальную валидацию и обработку инструкций
        for cmd in commands:
            if cmd.startswith('TYPE'):
                self.plugin_type = cmd.split()[1]

                self.logger.debug(f'Set plugin type : {self.plugin_type}')

            elif cmd.startswith('PAYLOAD'):
                self.payload_filename = cmd.split()[1]

                self.logger.debug(f"Set payload file : {self.payload_filename}")

            elif cmd.startswith('ENTRY'):
                classname, method = cmd.split()[1:]
                self.payload_classname = classname
                self.payload_method = method

                self.logger.debug(f"Set payload classname : {self.payload_classname}")
                self.logger.debug(f"Set payload class method : {self.payload_method}")

            elif cmd.startswith('REF'):
                self.reference_name = cmd.split()[1]

                self.logger.debug(f"Set unique reference name is {self.reference_name}")

            elif cmd.startswith('INIT'):
                match = re.match(r"^[A-Z]+\ +([a-zA-Z0-9_]+)\ +([A-Z]+)\((.*)\)", cmd)
                _key, _type, _value = tuple(match.groups())

                self.payload_init_keywords.append(EntryObject(_key, _type, _value))

                self.logger.debug(f"Set init payload parameter named: {_key} which type: {_type} represents: {_value} ")

            elif cmd.startswith('SET'):
                keyword, *param = cmd.split()[1:]
                if keyword == "restart-interval":
                    self.restart_interval = ' '.join(param)
                    self.logger.debug(f"Set restart interval is {param}")
                elif keyword == "LogMode":
                    self.logmod = param[0]
                    self.logger.debug(f"Set logging mode is {param}")

            elif cmd.startswith('ADD'):
                module, *params = cmd.split()[1:]

                _critical = bool(params and params[0].lower() == "critical")
                self.pipelines.append(Module(module, params, _critical))

                self.logger.debug(f"Add pipeline module named: {module}, with parameters: {params}")

            elif cmd.startswith('NEW_FLOW'):
                module, *params = cmd.split()[1:]
                self.bus_entities.append((module, params))

                self.logger.debug(f"Add new bus flow named: {module}, with parameters: {params}")

            elif cmd.startswith('FILE'):
                filename = cmd.split()[1]
                self.__plugin_files.append(filename)
                self.logger.debug(f'File of plugin named: {filename}')
