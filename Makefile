# Импорт параметров окружения
ifneq (,$(wildcard ./.env))
    include .env
    export
endif



localstorage:


filestorage:


database:


poetry:
	poetry --version
	poetry install


dev:
