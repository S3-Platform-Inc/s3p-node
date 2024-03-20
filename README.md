# NSPK DI Sources Parser Platform
![S3P logo](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/11cdcf7e-49b6-4276-acc6-1c863beac414)

## Virtual environment setup

Перед началом работы нужно настроить виртуальное пространство. За него отвечает Poetry.

1. Стянуть проект с [репозитория](https://github.com/CuberHuber/NSPK_DI_parser). Например через
   https: `git clone https://github.com/CuberHuber/NSPK_DI_parser.git`
2. Установить [poetry](https://python-poetry.org/docs/#installation)
3. установить зависимости `poetry install`
4. запустить виртуальное окружение `poetry shell`

## Usage

Перед использоваением нужно настроить виртуальное окружение

1. запустить главный файл из cmd `poetry run python main.py`

## Links

- Трекер задач: https://github.com/users/CuberHuber/projects/5
- Документация: https://docs.google.com/document/d/1onPsC6dvRas5m2kFdzOmeXL2HEhkeMU3Izzs-rsJsXM/edit?usp=sharing
- Miro доска:   https://miro.com/app/board/uXjVMcNMDsQ=/?share_link_id=864982821677

## Test

Перед тестированием платформы нужно:

1. Скачать виртуальное окружение [Poetry](https://python-poetry.org/)
2. Скачать docker и docker-compose. Если рабочая машина Windows, то Docker Hub
3. Скачать [make](https://www.technewstoday.com/install-and-use-make-in-windows/)
4. Если ты работаешь в PyCharm, то он (после скачивания poetry) должен сам предложить настроить виртуальное окружение.
   Ну, либо poetry install.
5. `cp .env.dev.example .env` в корне проекта в терминале
6. Теперь нужно вставить путь до плагина SPP. Плагин можно хранить в любом месте на пк. В корне проекта в
   файле `main.py` нужно указать полный путь ([Как работать с PyCharm](#работа-с-pycharm))

```python
plugin_path = < absolute_path_до_плагина >
```

7. Теперь можно запускать платформу. это можно сделать несколькими способами
    1. ~~_Это запустить main.py через IDEA. Пока не актуально_~~
    2. в терминале в корне прописать `make dev`

Вообще, если хочется трейсануть код и посмотреть что как работает, то можно юзать main.py из идеешки, но перед этим *
*ОБЯЗАТЕЛЬНО ЗАПУСТИТЬ** `make dev`

### Плагины

Все плагины создаются на основе [Плагина отца](https://github.com/CuberHuber/NSPK-DI-SPP-plugin-template).
Для удобства тестирования рекомендуется стягивать репозиторий плагина на локальную машину. Затем, в пункте [4](#test)
указать прямой путь до корня скачанного проекта.
