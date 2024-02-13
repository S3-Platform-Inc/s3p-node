from src.spp.types import SPP_plugin
from . import psConnection


class Plugin:
    """
    Схема плагина для взаимодействия с базой данных
    """

    @staticmethod
    def relevant_plugin(_type: str) -> SPP_plugin:
        """
        Получения релевантного плагина.
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
        with psConnection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'public.relevant_plugin_for_processing', (_type,))
                output = cursor.fetchone()
                if output:
                    return SPP_plugin(
                        plugin_id=output[0],
                        repository=output[1],
                        active=True,
                        pub_date=output[2],
                        type=output[3],
                    )
                raise ValueError('No relevant plugins')


if __name__ == "__main__":
    ...
