# Импорт параметров окружения
ifneq (,$(wildcard ./.env))
    include .env
    export
endif




docker: | db ftpstorage
	timeout 2
	docker-compose up -d


# Временный каталог для данных СУБД
# .env $(DB_BASE_TEMP_DIR)
db:
	@mkdir $@

# Временный каталог для данных локального хранилища
# .env $(LS_BASE_TEMP_DIR)
localstorage:
	@mkdir $@
	@mkdir "$(LS_BASE_TEMP_DIR)/$(LS_WORK_DIR)"

# Временный каталог для данных FTP сервера
# .env $(FS_BASE_TEMP_DIR)
ftpstorage:
	@mkdir $@
	@mkdir "$(FS_BASE_TEMP_DIR)/$(FS_WORK_DIR)"

# Инициализация базы данных. Зависит от запущенного докера и скрипта инициализации
database-init: docker scripts/db/init_and_create.sql
#	Переходим в папку для
#	Прошу прощение за говнокод. Позде придумаю как ожидать необходимое время
	timeout 20
	docker-compose -f docker-compose.yml exec $(DB_DOCKER_SERVICE_NAME) psql -U $(DB_USER) -d $(DB_DATABASE) -f $(DB_INIT_FILE)


poetry: pyproject.toml poetry.lock
	poetry --version
	poetry install

dev: main.py database-init | localstorage
	poetry run python main.py

# Выключает и удаляет все контейнеры, удаляет временные каталоги и файлы
clean: | db localstorage ftpstorage
	docker-compose down

	@rmdir /Q /S $(DB_BASE_TEMP_DIR)
	@rmdir /Q /S $(LS_BASE_TEMP_DIR)
	@rmdir /Q /S $(FS_BASE_TEMP_DIR)
