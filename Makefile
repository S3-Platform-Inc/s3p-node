# Импорт параметров окружения
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Получения имени ОС
OS := $(shell uname)
current-os:
	@echo "$(OS) os. Use 'make dev' to init dev db"

ifeq ($(OS), Darwin)
##################################
#       Run MacOS commands       #
##################################

# Make Localstorage Directory
$(LS_BASE_TEMP_DIR):
	@mkdir $@

# Plugin Archive Directory
$(PL_BASE_TEMP_DIR):
	@mkdir $@

# Logs Directory
$(SPP_LOG_TEMP_PATH):
	@mkdir $@

docker: | setup-env-files
	$(shell docker-compose up -d --build)

docker-dev: | setup-env-files
	$(shell docker-compose -f docker-compose-dev.yml up -d --build)

clean:
	$(shell docker-compose down)
	$(shell rm -rf $(DB_BASE_TEMP_DIR))
	$(shell rm -rf $(LS_BASE_TEMP_DIR))
	$(shell rm -rf $(PL_BASE_TEMP_DIR))
	$(shell rm -rf $(SPP_LOG_TEMP_PATH))

dev: main.py | setup-env-files
	poetry run python main.py

current-os:
	@echo $(OS)

endif

poetry: pyproject.toml poetry.lock
	poetry --version
	poetry install

setup-env-files: $(LS_BASE_TEMP_DIR) $(PL_BASE_TEMP_DIR) $(SPP_LOG_TEMP_PATH)

setup-dependencies: | setup-env-files
