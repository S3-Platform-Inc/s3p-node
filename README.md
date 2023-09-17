# NSPK DI Sources Parser Platform

![2](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/e4328b34-67f6-4427-8629-355c72af04e2)

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

### Работа с PyCharm

Чтобы удобно тестировать и работать с платформой и плагином одновременно, предлагается добавить в текущий проект
платформы дополнительный проект плагина.

1. Идем в пункт меню и называем `Open`

![photo_3_2023-07-22_11-18-18](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/300821d1-87fa-4930-ac06-121031399ad4)

2. Выбираем каталог с проектом плагина

![photo_2_2023-07-22_11-18-18](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/32a8e51c-48d0-435d-8248-327121c9247d)

3. Далее выбираем `Attach`.

![photo_6_2023-07-22_11-18-18](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/5e658107-a20e-432f-86ee-c116c9971b55)

4. Гуд, теперь рядом с проектом платформы лежит проект плагина.

![photo_1_2023-07-22_11-18-18](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/80cb82c9-aace-4f1c-b5c5-5e825bcd8201)

5. Жмем `пкм` по папке плагина и копируем абсолютный путь

![photo_7_2023-07-22_11-18-18](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/440fea02-b47f-43c9-a05c-4707e7ae6ba4)

7. Возвращаемся к процессу настройки платформы

![photo_5_2023-07-22_11-18-18](https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform/assets/34835155/70877cb4-2724-42cf-8885-d15b7ae09392)
