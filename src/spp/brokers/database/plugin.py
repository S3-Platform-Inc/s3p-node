import asyncio
import datetime

from sqlalchemy import text

from spp.types import SPP_plugin
from . import sync_get_engine, _datetime_param


class Plugin:
    """
    Схема плагина для взаимодействия с базой данных
    """

    @staticmethod
    def all_active() -> list[SPP_plugin]:
        """
        Получение данных о всех активных плагинов.
        :return:
        :rtype:
        """
        plugins = asyncio.run(Plugin.__get_all_active_plugins())
        res: list[SPP_plugin] = []
        for row in plugins:
            res.append(SPP_plugin(
                plugin_id=row[0],
                repository=row[1],
                active=row[2],
                pub_date=row[3]
            ))
        return res

    @staticmethod
    def relevant_plugins() -> list[SPP_plugin]:
        """
        Получения всех релевантных плагинов.
        Плагин считается релевантным если:
        1. Он активный
        И
        2.
            2.1. Задача, связанная с плагином не существует
                ИЛИ
            2.2. Задача, связанная с плагином в состоянии (FINISHED или BROKEN) и время запуска < текущего
        :return:
        :rtype:
        """
        plugins = asyncio.run(Plugin.__relevant_plugins_for_processing())
        res: list[SPP_plugin] = []
        for row in plugins:
            res.append(SPP_plugin(
                plugin_id=row[0],
                repository=row[1],
                active=True,
                pub_date=row[2]
            ))
        return res

    @staticmethod
    def set_pub_date(plugin: SPP_plugin, new_pub_date: datetime.datetime):
        """
        Обновления даты публикации плагина
        :param plugin:
        :type plugin:
        :param new_pub_date:
        :type new_pub_date:
        :return:
        :rtype:
        """
        asyncio.run(Plugin.__set_plugin_pub_date(plugin.plugin_id, new_pub_date))

    @staticmethod
    def activate(plugin: SPP_plugin):
        """
        Метод активирует плагин
        :param plugin:
        :type plugin:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    def deactivate(plugin: SPP_plugin):
        """
        Метод деактивирует плагин
        :param plugin:
        :type plugin:
        :return:
        :rtype:
        """
        ...

    @staticmethod
    async def __get_all_active_plugins() -> list[tuple]:
        """
        Асинхронное получение всех активных плагинов
        :return:
        :rtype:
        """
        async with sync_get_engine().begin() as conn:
            query_param = """SELECT * FROM public.get_all_active_plugins();"""
            result = await conn.execute(text(query_param))
            await conn.commit()
        return result.fetchall()

    @staticmethod
    async def __set_plugin_pub_date(_id: int, pub_date: datetime.datetime):
        """
        Асинхронное обновление даты публикации плагина
        :param _id:
        :type _id:
        :param pub_date:
        :type pub_date:
        :return:
        :rtype:
        """
        async with sync_get_engine().begin() as conn:
            query_param = f"SELECT * FROM public.set_plugin_pub_date(" \
                          f"{_id}," \
                          f"{_datetime_param(pub_date)}" \
                          f");"
            result = await conn.execute(text(query_param))
            await conn.commit()
        return result.fetchall()

    @staticmethod
    async def __relevant_plugins_for_processing() -> list[tuple]:
        async with sync_get_engine().begin() as conn:
            query_param = f"SELECT * FROM public.relevant_plugins_for_processing();"
            result = await conn.execute(text(query_param))
            await conn.commit()
        return result.fetchall()


if __name__ == "__main__":
    aas = Plugin.all_active()
    print(aas)
