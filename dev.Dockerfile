FROM python:3.11.5-alpine

# базовая директория контейнера
WORKDIR /sppnode

# копирование файлов пакетного менеджера в контейнер
COPY pyproject.toml poetry.lock ./

# установка пакетного менеджера poetry фиксированной версии (1.6.1)
RUN python -m pip install --no-cache-dir poetry==1.6.1

# установка библиотеки для python magic и драйвера для selenium
# RUN apk update && apk add -y --no-install-recommends --no-cache libmagic chromium-chromedriver curl
RUN apk update && apk add -y --no-install-recommends --no-cache libmagic chromium-chromedriver

#RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#    unzip chromedriver_linux64.zip -d /usr/bin && \
#    chmod +x /usr/bin/chromedriver && \
#    rm chromedriver_linux64.zip

# установка зависимостей в виртуальное окружение poetry
RUN poetry install --no-directory --no-root --no-interaction

# Создание необходимых директорий в контейнере:
#   [] /logs - для хранения логов
#   [] /plugin_archive - для хранения загруженных плагинов
#   [] /localstorage - для файлов локального хранилища
RUN mkdir -p ./logs && mkdir -p ./plugin_archive && mkdir -p ./localstorage

# копирование исходного кода, main файла, скриптов, конфигураций, .env файл
COPY src ./src
COPY main.py ./
COPY scripts ./scripts
COPY configurations ./configurations
COPY .env ./.env
COPY ./node.yaml ./node.yaml

# запуск узла SPP
CMD ["poetry", "run", "python", "main.py"]

