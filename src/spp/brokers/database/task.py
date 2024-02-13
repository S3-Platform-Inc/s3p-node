import datetime

from src.spp.types import SPP_plugin
from .main import psConnection, interval


class Task:
    """
    Схема плагина для взаимодействия с базой данных
    """

    @staticmethod
    def create(plugin: SPP_plugin, time_start: datetime.datetime | None = None, status_code: int | None = None) -> int:
        """
        Получение данных о всех активных плагинов.
        :return: ID Задачи (Task)
        :rtype:
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.create_task', (int(plugin.plugin_id), time_start, status_code))
                output = cursor.fetchone()
                print(f'Create task. ID {output[0]}')
                return output[0]

    @staticmethod
    def status_update(plugin: SPP_plugin, status: int):
        """
        Обновления даты публикации плагина
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.set_task_status', (int(plugin.plugin_id), int(status)))
                cursor.fetchone()

    @staticmethod
    def finish(plugin: SPP_plugin, restart_interval: str | None):
        """
        Завершение работы задачи и установка времени перезапуска
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.task_finish', (int(plugin.plugin_id), interval(restart_interval)))
                cursor.fetchone()

    @staticmethod
    def broke(plugin: SPP_plugin):
        """
        Выпадение ошибки в задаче на различных этапах
        """
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.task_broke', (int(plugin.plugin_id),))
                cursor.fetchone()


if __name__ == "__main__":
    t = Task.create(SPP_plugin(1, 'qrwer', True, None), status_code=20)
    print(t)
