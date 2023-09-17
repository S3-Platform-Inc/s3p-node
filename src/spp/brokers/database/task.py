import asyncio
import datetime

import sqlalchemy.exc
from sqlalchemy import text

from spp.types import SPP_plugin
from .main import sync_get_engine, _def_null_param, _datetime_param, _interval_param


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
        task = asyncio.run(Task.__create_task(plugin.plugin_id, time_start, status_code))
        print(task)
        return task

    @staticmethod
    def set_status(plugin: SPP_plugin, status: int):
        """
        Обновления даты публикации плагина
        :param status:
        :type status:
        :param plugin:
        :type plugin:
        :return:
        :rtype:
        """
        asyncio.run(Task.__set_task_status(plugin.plugin_id, status))

    @staticmethod
    def finish(plugin: SPP_plugin, restart_interval: str | None):
        """
        Завершение работы задачи.
        :param plugin:
        :type plugin:
        :param restart_interval:
        :type restart_interval:
        :return:
        :rtype:
        """
        asyncio.run(Task.__finish_task(plugin.plugin_id, restart_interval))

    @staticmethod
    async def __create_task(plugin_id: int, time_start: datetime.datetime | None, status_code: int | None) -> int:
        """
        Асинхронное получение всех активных плагинов
        :return:
        :rtype:
        """
        try:
            async with sync_get_engine().begin() as conn:
                query_param = f"SELECT * FROM public.create_task(" \
                              f"{plugin_id}, " \
                              f"{_def_null_param(_datetime_param(time_start))}, " \
                              f"{_def_null_param(status_code)}" \
                              f");"
                result = await conn.execute(text(query_param))
                await conn.commit()
            return result.fetchall()
        except sqlalchemy.exc.DBAPIError as e:
            print(e)
            return 1
        except Exception as e:
            raise e

    @staticmethod
    async def __set_task_status(_id: int, status: int) -> bool:
        """
        Асинхронное обновление даты публикации плагина
        :param _id:
        :type _id:
        :return:
        :rtype:
        """
        async with sync_get_engine().begin() as conn:
            query_param = f"SELECT * FROM public.set_task_status(" \
                          f"{_id}, " \
                          f"{status}" \
                          f");"
            result = await conn.execute(text(query_param))
            await conn.commit()
        return result.fetchall()

    @staticmethod
    async def __finish_task(_id: int, restart_time: str | None):
        async with sync_get_engine().begin() as conn:
            query_param = f"SELECT * FROM public.task_finish(" \
                          f"{_id}, " \
                          f"{_def_null_param(_interval_param(restart_time))}" \
                          f");"
            result = await conn.execute(text(query_param))
            await conn.commit()
        return result.fetchall()


if __name__ == "__main__":
    t = Task.create(SPP_plugin(1, 'qrwer', True, None), status_code=20)
    print(t)
