import datetime

from src.spp.types import SppPlugin, SppNode, SppTask, SppRefer
from .main import ps_connection


class Task:
    """
    Схема плагина для взаимодействия с базой данных
    """
    schema = 'tasks'

    @staticmethod
    def create(plugin: SppPlugin, time_start: datetime.datetime | None = None, status_code: int | None = None) -> int:
        """
        Получение данных о всех активных плагинов.
        :return: ID Задачи (Task)
        :rtype:
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.create_task', (int(plugin.id), time_start, status_code))
                output = cursor.fetchone()
                print(f'Create task. ID {output[0]}')
                return output[0]

    @staticmethod
    def relevant(node: SppNode) -> SppTask:
        """
        Получение релевантной задачи
        :param node:
        :return:
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.relevant', (node.id, ))
                output = cursor.fetchone()
                if output:
                    return SppTask(
                        id=output[1],
                        session_id=output[0],
                        status=output[2],
                        plugin=SppPlugin(
                            id=output[3],
                            repository=output[4],
                            active=True,
                            loaded=output[5],
                            config=output[6],
                            type=output[7],
                        ),
                        refer=SppRefer(output[8], output[9], output[7], None)
                    )
                raise ValueError('No relevant tasks')

    @staticmethod
    def status_update(task: SppTask, status: int):
        """
        Обновления даты публикации плагина
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.set_status', (task.id, int(status)))
                cursor.fetchone()

    @staticmethod
    def finish(node: SppNode, task: SppTask):
        """
        Завершение работы задачи и установка времени перезапуска
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.finish', (node.id, task.session_id))
                cursor.fetchone()

    @staticmethod
    def broke(node: SppNode, task: SppTask, e: Exception):
        """
        Выпадение ошибки в задаче на различных этапах
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.broke', (int(node.id), task.session_id, str(e)))
                cursor.fetchone()


if __name__ == "__main__":
    ...
