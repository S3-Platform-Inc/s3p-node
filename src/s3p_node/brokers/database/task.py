import datetime

from s3p_sdk.types import S3PPlugin, S3PNode, S3PTask, S3PRefer

from src.s3p_node.exceptions.triggers.no_relevant_tasks import NoRelevantTasks
from .main import ps_connection


class Task:
    """
    Схема плагина для взаимодействия с базой данных
    """
    schema = 'tasks'

    @staticmethod
    def create(plugin: S3PPlugin, time_start: datetime.datetime | None = None, status_code: int | None = None) -> int:
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
    def relevant(node: S3PNode) -> S3PTask:
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
                    return S3PTask(
                        id=output[1],
                        session_id=output[0],
                        status=output[2],
                        plugin=S3PPlugin(
                            id=output[3],
                            repository=output[4],
                            active=True,
                            loaded=output[5],
                            config=output[6],
                            type=output[7],
                            # version=output[8],
                            version=None,
                        ),
                        refer=S3PRefer(output[8], output[9], output[7], None)
                    )
                raise NoRelevantTasks(node)

    @staticmethod
    def status_update(task: S3PTask, status: int):
        """
        Обновления даты публикации плагина
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.set_status', (task.id, int(status)))
                cursor.fetchone()

    @staticmethod
    def finish(node: S3PNode, task: S3PTask):
        """
        Завершение работы задачи и установка времени перезапуска
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.finish', (node.id, task.session_id))
                cursor.fetchone()

    @staticmethod
    def broke(node: S3PNode, task: S3PTask, e: Exception):
        """
        Выпадение ошибки в задаче на различных этапах
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.broke', (int(node.id), task.session_id, str(e)))
                cursor.fetchone()


if __name__ == "__main__":
    ...
