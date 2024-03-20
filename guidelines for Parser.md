```python
class <parser name>:
    
    SOURCE_NAME = 'uniq source name'
    _content_document: list[SPP_document]

    def __init__(self, webdriver, max_count_documents: int = None, last_document: SPP_document = None, *args, **kwargs):
        """
        Конструктор класса парсера
    
        По умолчанию внего ничего не передается, но если требуется (например: driver селениума), то нужно будет
        заполнить конфигурацию
        
        - webdriver: драйвер селениума, с помощью которого парсер будет работать
        (если парсер работает через библиотеку selenium)
        
        - max_count_documents:int: параметр максимального количества документов, которые ждем платформа от парсера.
        Парсер обязан отдавать список документов длиной не более max_count_documents.
        
        - last_document:SPP_document: последний документ обрабатываемого источника.
        Парсер обязан прекратить свою работу, если встретил этот документ при своей работе.
        """
        # Обнуление списка
        self._content_document = []
        self._driver = webdriver
        self._max_count_documents = max_count_documents
        self._last_document = last_document
    
        # Логер должен подключаться так. Вся настройка лежит на платформе
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f"Parser class init completed")
        self.logger.info(f"Set source: {self.SOURCE_NAME}")
        ...

    def content(self) -> list[SPP_document]:
        """
        Главный метод парсера. Его будет вызывать платформа. Он вызывает метод _parse и возвращает список документов
        :return:
        :rtype:
        """
        self.logger.debug("Parse process start")
        try:
            self._parse()
        except Exception as e:
            self.logger.debug(f'Parsing stopped with error: {e}')
        else:
            self.logger.debug("Parse process finished")
        return self._content_document

    def _parser(cls, *args, **kwargs): ...

    @staticmethod
    def _find_document_text_for_logger(doc: SPP_document):
        """
        Единый для всех парсеров метод, который подготовит на основе SPP_document строку для логера
        :param doc: Документ, полученный парсером во время своей работы
        :type doc:
        :return: Строка для логера на основе документа
        :rtype:
        """
        return f"Find document | name: {doc.title} | link to web: {doc.web_link} | publication date: {doc.pub_date}"

    def find_document(self, _doc: SPP_document):
        """
        Метод для обработки найденного документа источника.
        Рекомендованный для всех парсеров
        """
        if self._last_document and self._last_document.hash == _doc.hash:
            raise Exception(f"Find already existing document ({self._last_document})")

        if self._max_count_documents and len(self._content_document) >= self._max_count_documents:
            raise Exception(f"Max count articles reached ({self._max_count_documents})")

        self._content_document.append(_doc)
        self.logger.info(self._find_document_text_for_logger(_doc))
```


### Middleware
В разделе Middleware необходимо указать модули и их конфигурацию в порядке выполнения [, а также расширенную шины]    

#### Modules
Модули указываются в массиве по ключу `modules`.
Структура конфигурации модуля следующая:
```
{
    "order": number,
    "name": "Module name",
    "critical": boolean flag,
    "params": {
        key1: value1,
        ...
        keyn: valuen
    }},
```
- `order` содержит число приоритета исполнения. Модули исполняются платформой по этому приоритету.
- `name` содержит имя класса модуля в платформе. Необходимо сверить значение со списком поддерживаемых модулей.
- `critical` параметр, который означает критичность модуля при обработке источника. Если этот модуль прерывает исполнение с ошибкой, то платформа останавливает исполнение задачи.
- `params` содержит конфигурацию для модуля в формате json объекта. Эта конфигурация в формате dict будет загружена в модуль на этапе его инициализации. В значениях можно использовать только простые типы. 

#### bus
Этот раздел пока не обрабатывается SPP Node

### Plugin
В разделе Plugin необходимо указать настройки плагина непосредственно

```json
{
"plugin": {
    "reference": reference name,
    "type": <type of plugin>,
    "filenames": [
      "filename 1",
      "filename 2",
      ...
      "filename N"
    ],
    "localstorage": boolean
}
```
- `reference` содержит уникальное имя названия объекта, на который ссылается плагин. Для плагинов-парсеров таким объетом будет источник. Для плагинов-ml таким объектом будет модель ml.
- `type` содержит тип плагина. Если мы используем парсер, то пишем `SOURCE`, если используем ml - `ML`
- `filenames` содержит массив имен файлов плагина в текстовом виде, которые будут подгружены из репозитория плагина после инициализации при его подготовке.
- `localstorage` boolean параметр, который говорит: использовать локальное хранилище для этого плагина или нет. Значение по умолчанию - `false`.


### Task
В разделе Task необходимо настроить поведение задачи, которая будет создаваться для выполнения плагина.
```json
{
    "log": -1,
    "trigger": {
      "type": "SCHEDULE",
      "interval": interval
    }
}
```
- `log` параметр определяющий уровень логирования для задачи. _*сейчас не используется_.
- `trigger` объект, определяющий условие активации задачи плагина.
  - `type` тип активации. Пока доступен только тип `SCHEDULE`
  - `interval` параметр временного интервала. Определяет интервал, через который будет запущена задача после прошлого завершения. Записывается в формате SQL interval

### Payload
В разделе Payload необходимо указать объект нагрузки, который будет запускаться платформой.

#### Структура конфигурации Payload
```json
{
    "file": "file name",
    "class": "class name",
    "entry": {
        "point": "method name",
        "params": array
    }
}
```
- `file` содержит имя файла, из которого платформа должна взять класс. Этот файл загружается в момент подготовки плагина и этот файл должен быть указан в поле `plugin` -> `filenames[]`.
- `class` содержит имя класса, который должна загрузить платформа.
- `entry` содержит конфигурацию точки входа класса нагрузки
  - `point` содержит имя метода, который должен вернуть объект. Этот объект по умолчанию кладется в поток `documents` шины.
  - `params` содержит объекты, которые должны быть переданы в конструктор при инициализации класса нагрузки

#### Payload params
```json
{
  "key": "key word",
  "value": {
      "type": "type of param", 
      "name": "value or name a param",
      "bus": boolean
  }
}
```
- `key` ключ, по которому платформа будет передавать параметр в конструктор
- `value` значение, которое будет передано
  - `type` означает тип передаваемого параметра. Платформа поддерживает 3 типа:
    - **module** - объект является модулем
    - **file** - объект байтового представления файла *(Файл должен быть указан в поле `plugin` -> `filenames[]`)
    - **const** - постоянная переменная, которая указывается из конфигурации (массив, число, строка, словарь, прочие базовые типы)
  - `name` значение объекта или имя модуля, или файла
  - `bus` флаг, который показывает о необходимости передачи ссылки на объект шины в конструктор при инициализации класса модуля. В платформе есть 2 типо модулей: те, что ожидают шину и работают с ней, и те, кому не требуется шина для работы. 


### Пример конфигурации тестового плагина
```json
{
"plugin": {
    "reference": "test1",
    "type": "SOURCE",
    "filenames": ["testcase1.py"],
    "localstorage": true
},
"task": {
    "log": -1,
    "trigger": {
      "type": "SCHEDULE",
      "interval": "1 minute"
    }
},
"middleware": {
    "modules": [
        { "order": 1, "name": "TimezoneSafeControl", "critical": true, "params": {}},
        { "order": 2, "name": "CutJunkCharactersFromDocumentText", "critical": true, "params": {
          "fields": ["web_link"]
        }},
        { "order": 3, "name": "FilterOnlyNewDocumentWithDB", "critical": true, "params": {}},
        { "order": 4, "name": "SaveDocumentToDB", "critical": true, "params": {}}
    ],
    "bus": {
        "entities": []
    }
},
"payload": {
    "file": "testcase1.py",
    "class": "TESTParserCase1",
    "entry": {
        "point": "content",
        "params": [
          {"key": "last_document", "value": {"type": "module", "name": "LastDocumentBySrc", "bus": true}}
        ]
    },
    "additional_methods": null
}
}

```