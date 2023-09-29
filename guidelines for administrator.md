# Руководство администратора Sources Parser Platform


# DEV: Установка и настройка

1. Скачаем исходный код из репозитория`git clone https://github.com/CuberHuber/NSPK-DI-Sources-Parser-Platform.git` или `git@github.com:CuberHuber/NSPK-DI-Sources-Parser-Platform.git`
2. Перейдем в каталог `cd NSPK-DI-Sources-Parser-Platform`
3. Перейдем на рабочую ветку `git checkout platform-synchronous`
4. `cp .env.dev.example .env`
5. Заполнить `.env` файл по шаблону
6. Поднимем инфраструктуру `make setup-dependencies`
7. Можно запускать main.py (в зависимости от IDE)