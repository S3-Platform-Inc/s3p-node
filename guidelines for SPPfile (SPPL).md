# Source Parser Platform Language

Source Parser Platform Language / SPP Language / SPPL - это **_декларативный_** язык для конфигурации SPP по отношению
к парсеру, результату его работу, а также к _**задаче (Task)**_.
___

## Сущности

SPPL описывает, накладывает правила или манипулирует определенными сущностями, как неделимыми объектами.\
Такими объектами могут быть:

1. Задача (Task)
2. Парсер
3. Модуль
   ([SPP_module](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/source_parser_platform/module/spp_module.py))
4. Шина
   ([Bus](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/source_parser_platform/bus/bus.py))

### Формат описания SPPfile

```dockerfile
INSTRUCTION *arguments
```

### Подключение источника и парсера

```mysql
SOURCE <Уникальное название источника>

PARSER <Название файла парсера без .py>
```

Уникальное название источника будет использоваться:

- в запросах к базе данных;
- при взаимодействии с хранилищами (файлов или локальным);
- при журналировании.

### Комментирование

```mysql
# This plugin processes File source
# Link: <link to source>
# Author:
#	Roman Lupashko
#	NSPK DI
```

### Настройки окружения задачи

```
SETENV <название атрибута>, [<параметры атрибута>,]

```

### Настройка шины

По умолчанию шина содержит 7 постоянных потока (сущности):

1. настройки
   ([options](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/sources_parser_platform/bus/flow/entity/options.py))
2. документы
   ([documents](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/sources_parser_platform/bus/flow/entity/documents.py))
3. источник
   ([source](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/sources_parser_platform/bus/flow/entity/source.py))
4. база данных
   ([database](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/sources_parser_platform/bus/flow/entity/database.py))
5. файловый сервер
   ([fileserver](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/sources_parser_platform/bus/flow/entity/fileserver.py))
6. локальное хранилище
   ([local_storage](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/blob/sources_parser_platform/src/sources_parser_platform/bus/flow/entity/local_storage.py))
7. Журналирование (logging)

Но, при необходимости, можно поместить в шину кастомный поток с необходимой сущностью

```mysql
BUS_ADD <Название потока> <сущность>
```

### Настройка парсера

```mysql
INIT <keyword параметра для инициализации класса парсера> <сущность или переменная>
START
<название класса парсера> <метод для получения списка документов>
```

Если для инициализации класса парсера нужны настраиваемые параметры, то их нужно указать
с использованием инструкции ```INIT```.

### Настройка обработки

```mysql
ADD <Название модуля> [<вариативные параметры>, ]
```

## Пример SPPfile для источника PCI

```mysql
# This plugin processes File source
# Link: https://www.pcisecuritystandards.org
# Author:
#	Roman Lupashko
#	NSPK DI

SOURCE pci

PARSER pci

SETENV LogMode debug

BUS_ADD s_download PARSER/PCI/temp_download

INIT driver WebDriver
START
PCI content

ADD FilterOnlyNewDocumentWithDB
ADD DownloadDocumentsThroughSeleniumTemp
ADD ExtractTextFromFile
ADD UploadDocumentToDB

```