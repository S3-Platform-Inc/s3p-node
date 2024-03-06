from . import Config
from .schemes import Plugin, Task, Middleware, Payload, Module, EntryObject


class ParseConfig:

    def __init__(self, config: dict):
        self._config = config
        self._zero_keys = ['plugin', 'task', 'middleware', 'payload']
        ...

    def config(self) -> Config:
        return self._verify(self._parse())

    def _verify(self, config: Config) -> Config:
        """
        Метод для валидации конфигурации. Добавить исключения при несоответствиях
        :param config:
        :return:
        """
        return config

    def _parse(self) -> Config:
        for key in self._config.keys():
            if key not in self._zero_keys:
                raise KeyError(f'Invalid key: {key} in the plugin`s config')
            continue

        pl = self._config.get('plugin')
        t = self._config.get('task')
        md = self._config.get('middleware')
        p = self._config.get('payload')
        print(f'plugin ------------------------\n\r'
              f'  |  reference      |   {pl.get("reference")}\n\r'
              f'  |  type           |   {pl.get("type")}\n\r'
              f'  |  filenames      |   {tuple(pl.get("filenames"))}\n\r'
              f'  |  localstorage   |   {pl.get("localstorage")}\n\r'
              f'-------------------------------')

        print(f'task --------------------------\n\r'
              f'  |  log            |   {t.get("log")}\n\r'
              f'  |  trigger        |   {t.get("trigger").get("interval")}\n\r'
              f'-------------------------------')

        print(f'middleware --------------------\n\r'
              f'  |  modules        |   {tuple(md.get("modules"))}\n\r'
              f'  |  bus            |   {tuple(md.get("bus").get("entities"))}\n\r'
              f'-------------------------------')

        print(f'payload --------------------\n\r'
              f'  |  file               |   {p.get("file")}\n\r'
              f'  |  class_name         |   {p.get("class")}\n\r'
              f'  |  entry_points       |   {p.get("entry").get("point")}\n\r'
              f'  |  entry_params       |   {tuple(p.get("entry").get("params"))}\n\r'
              f'  |  additional_methods |   {p.get("additional_methods")}\n\r'
              f'-------------------------------')
        return Config(
            plugin=Plugin(
                reference=pl.get("reference"),
                type=pl.get("type"),
                filenames=tuple(pl.get("filenames")),
                localstorage=pl.get("localstorage")
            ),
            task=Task(
                log=t.get("log"),
                trigger=t.get("trigger").get("interval")
            ),
            middleware=Middleware(
                modules=tuple(
                    [Module(
                        order=m.get("order"),
                        name=m.get("name"),
                        critical=m.get("critical"),
                        options=m.get("params")
                    ) for m in md.get("modules")]),
                bus=tuple(md.get("bus").get("entities"))
            ),
            payload=Payload(
                file=p.get("file"),
                class_name=p.get("class"),
                entry_point=p.get("entry").get("point"),
                entry_params=tuple([EntryObject(
                    key=param.get("key"),
                    type=param.get("value").get("type"),
                    value=param.get("value").get("name")
                ) for param in p.get("entry").get("params")]),
                additional_methods=p.get("additional_methods")
            )
        )
