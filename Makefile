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
	@mkdir "$(DEV_LS_BASE_TEMP_DIR)/$(DEV_LS_WORK_DIR)"

# Временный каталог для данных FTP сервера
# .env $(FS_BASE_TEMP_DIR)
ftpstorage:
	@mkdir $@
	@mkdir "$(DEV_FS_BASE_TEMP_DIR)/$(DEV_FS_WORK_DIR)"

# Инициализация базы данных. Зависит от запущенного докера и скрипта инициализации
database-init: docker scripts/db/init_and_create.sql
#	Переходим в папку для
#	Прошу прощение за говнокод. Позде придумаю как ожидать необходимое время
	timeout 20
	docker-compose -f docker-compose.yml exec $(DEV_DB_DOCKER_SERVICE_NAME) psql -U $(DEV_DB_USER) -d $(DEV_DB_DATABASE) -f $(DEV_DB_INIT_FILE)


poetry: pyproject.toml poetry.lock
	poetry --version
	poetry install

dev: main.py database-init | localstorage
	poetry run python main.py

# Выключает и удаляет все контейнеры, удаляет временные каталоги и файлы
clean: | db localstorage ftpstorage
	docker-compose down

	@rmdir /Q /S $(DEV_DB_BASE_TEMP_DIR)
	@rmdir /Q /S $(DEV_LS_BASE_TEMP_DIR)
	@rmdir /Q /S $(DEV_FS_BASE_TEMP_DIR)
