import logging

INSTRUCTIONS = (
    "PARSER",
    "FROM",
    "SETENV",
    "START",
    "ADD",
    "INIT",
    "RETURN",
    "SOURCE",
    "BUS_ADD",
)


class SPPL_parse:
    __vars: dict = {}

    source_name: str

    parser_filename: str
    parser_classname: str
    parser_method: str
    parser_init_keywords: list = []

    bus_entities: list = []

    pipelines: list = []

    def __init__(self, src: str | list[str]):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.logger.debug("SPPfile parser start")
        self.__parse(self.__prepare_useful_commands(src))
        self.logger.debug("SPPfile parser finished")

    def __prepare_useful_commands(self, text) -> list[str]:
        useful_lines: list[str] = []
        # Выбирает те строки, в которых есть полезные команды из списка команд
        if isinstance(text, list):
            for line in text:
                if any(line.startswith(instruction) for instruction in INSTRUCTIONS):
                    line = line.replace('\n', '')
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

            elif cmd.startswith('SETENV'):
                ...

            elif cmd.startswith('ADD'):
                module, *params = cmd.split()[1:]
                self.pipelines.append((module, params))

                self.logger.debug(f"Add pipeline module named: {module}, with parameters: {params}")

            elif cmd.startswith('BUS_ADD'):
                module, *params = cmd.split()[1:]
                self.bus_entities.append((module, params))

                self.logger.debug(f"Add new bus flow named: {module}, with parameters: {params}")
