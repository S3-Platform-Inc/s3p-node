import datetime
from typing import Iterator, Any, Optional

from s3p_sdk.types import S3PPlugin, S3PNode, S3PTask, S3PRefer

from src.s3p_node.exceptions.triggers.no_relevant_tasks import NoRelevantTasks
from src.s3p_node.exceptions.triggers.no_current_task import NoCurrentTasks
from .main import ps_connection


class Task:
    """
    Схема плагина для взаимодействия с базой данных
    """
    schema = 'tasks'

    @staticmethod
    def parse_task(row: Iterator[Any]) -> S3PTask:
        return S3PTask(
            id=row[1],
            session_id=row[0],
            status=row[2],
            plugin=S3PPlugin(
                id=row[3],
                repository=row[4],
                active=True,
                loaded=row[5],
                config=row[6],
                type=row[7],
                version=None,
            ),
            refer=S3PRefer(row[8], row[9], row[7], None)
        )

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
                   return Task.parse_task(output)
                raise NoRelevantTasks(node)

    @staticmethod
    def start_session(tid: Optional[int], plid: Optional[int] = None) -> S3PTask:
        """
        Получение релевантной задачи
        :param tid:
        :param plid:
        :return:
        """
        with ps_connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{Task.schema}.start_session', (tid, plid))
                output = cursor.fetchone()
                if output:
                    return Task.parse_task(output)
                raise NoCurrentTasks(tid)

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
