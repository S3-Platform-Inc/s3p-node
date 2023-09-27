# Импорт параметров окружения
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Получения имени ОС
OS := $(shell uname)

ifeq ($(OS), Darwin)
##################################
#       Run MacOS commands       #
##################################

# Временный каталог для данных локального хранилища
# .env $(LS_BASE_TEMP_DIR)
$(LS_BASE_TEMP_DIR):
	@mkdir $@
	@mkdir -p "$(LS_BASE_TEMP_DIR)/$(LS_WORK_DIR)"

# Временный каталог для данных FTP сервера
# .env $(FS_BASE_TEMP_DIR)
$(FS_BASE_TEMP_DIR):
	@mkdir $@
	@mkdir -p "$(FS_BASE_TEMP_DIR)/$(FS_WORK_DIR)"

docker: | setup-env-files
	@sleep 2
	$(shell docker-compose up -d)

clean:
	$(shell docker-compose down)

	$(shell rm -rf $(DB_BASE_TEMP_DIR))
	$(shell rm -rf $(LS_BASE_TEMP_DIR))
	$(shell rm -rf $(FS_BASE_TEMP_DIR))
	$(shell rm -rf $(PL_BASE_TEMP_DIR))
	$(shell rm -rf $(SPP_LOG_TEMP_PATH))

# Инициализация базы данных. Зависит от запущенного докера и скрипта инициализации
database-init: docker scripts/db
#	Переходим в папку для
#	Прошу прощение за говнокод. Позде придумаю как ожидать необходимое время
	@while [ -z "$(shell docker-compose -f docker-compose.yml logs $(DB_DOCKER_SERVICE_NAME) 2>&1 | grep -o "ready to accept connections")" ]

	$(shell docker-compose -f docker-compose.yml exec $(DB_DOCKER_SERVICE_NAME) psql -U $(DB_USER) -d $(DB_DATABASE) -f $(DB_INIT_FILE))
	$(shell docker-compose -f docker-compose.yml exec $(DB_DOCKER_SERVICE_NAME) psql -U $(DB_USER) -d $(DB_DATABASE) -f $(DB_DATA_FILE))

else
ifeq ($(OS),Windows_NT)
##################################
#      Run Windows commands      #
##################################

# Временный каталог для данных локального хранилища
# .env $(LS_BASE_TEMP_DIR)
$(LS_BASE_TEMP_DIR):
	@mkdir $@
	@mkdir "$(LS_BASE_TEMP_DIR)/$(LS_WORK_DIR)"

# Временный каталог для данных FTP сервера
# .env $(FS_BASE_TEMP_DIR)
$(FS_BASE_TEMP_DIR):
	@mkdir $@
	@mkdir "$(FS_BASE_TEMP_DIR)/$(FS_WORK_DIR)"

docker: | $(DB_BASE_TEMP_DIR) $(FS_BASE_TEMP_DIR)
	timeout 2
	docker-compose up -d

# Выключает и удаляет все контейнеры, удаляет временные каталоги и файлы
clean: | $(DB_BASE_TEMP_DIR) $(LS_BASE_TEMP_DIR) $(FS_BASE_TEMP_DIR) $(PL_BASE_TEMP_DIR)
	docker-compose down

	@rmdir /Q /S $(DB_BASE_TEMP_DIR)
	@rmdir /Q /S $(LS_BASE_TEMP_DIR)
	@rmdir /Q /S $(FS_BASE_TEMP_DIR)
	@rmdir /Q /S $(PL_BASE_TEMP_DIR)
	@rmdir /Q /S $(SPP_LOG_TEMP_PATH)

# Инициализация базы данных. Зависит от запущенного докера и скрипта инициализации
database-init: docker scripts/db
#	Переходим в папку для
#	Прошу прощение за говнокод. Позде придумаю как ожидать необходимое время
	timeout 20
	docker-compose -f docker-compose.yml exec $(DB_DOCKER_SERVICE_NAME) psql -U $(DB_USER) -d $(DB_DATABASE) -f $(DB_INIT_FILE)
	docker-compose -f docker-compose.yml exec $(DB_DOCKER_SERVICE_NAME) psql -U $(DB_USER) -d $(DB_DATABASE) -f $(DB_DATA_FILE)

else
##################################
#       Run Linux commands       #
##################################


endif
endif

# Временный каталог для данных СУБД
# .env $(DB_BASE_TEMP_DIR)
$(DB_BASE_TEMP_DIR):
	@mkdir $@

# Временный каталог для хранения архивов плагинов
# .env $(PL_BASE_TEMP_DIR)
$(PL_BASE_TEMP_DIR):
	@mkdir $@

# Временный каталог для хранения логов
# .env $(SPP_LOG_TEMP_PATH)
$(SPP_LOG_TEMP_PATH):
	@mkdir $@

poetry: pyproject.toml poetry.lock
	poetry --version
	poetry install

setup-env-files: $(DB_BASE_TEMP_DIR) $(FS_BASE_TEMP_DIR) $(LS_BASE_TEMP_DIR) $(PL_BASE_TEMP_DIR)

setup-dependencies: database-init | setup-env-files

dev-docker:

dev: main.py | setup-env-files
	poetry run python main.py

dev-Pycharm: main.py database-init | setup-env-files
	poetry run python main.py

current-os:
	@echo $(OS)