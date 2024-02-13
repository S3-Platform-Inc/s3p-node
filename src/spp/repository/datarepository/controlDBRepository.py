import os

import psycopg2

from .abc_control_repository import AbcControlRepository
from ...types import SPP_plugin


class ControlDBRepository(AbcControlRepository):
    schema: str = 'public'

    def __init__(self): ...

    def next(self, plugin_type: str) -> SPP_plugin:
        """
        Returns relevant SPP_plugin from DB
        :param plugin_type: type of plugin. must be ALL / PARSER / ML
        :return: SPP_plugin object
        """
        with self._connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{self.schema}.relevant_plugin_for_processing', (plugin_type,))
                output = cursor.fetchone()
                return SPP_plugin(
                    plugin_id=output[0][0],
                    repository=output[0][1],
                    active=True,
                    pub_date=output[0][2],
                    type=output[0][3],
                )

    def status_update(self, plugin: SPP_plugin, status: int):
        """
        Update status of task by plugin ID.
        :param plugin:
        :param status:
        """
        with self._connection() as connection:
            with connection.cursor() as cursor:
                cursor.callproc(f'{self.schema}.set_task_status', (plugin.plugin_id, status))
                cursor.fetchone()

    def _connection(self):
        """
        Create a connection to the PostgreSQL Control-database
        :return:
        """
        return psycopg2.connect(
            database=self.DATABASE,
            user=self.USERNAME,
            password=self.PASSWORD,
            host=self.HOST,
            port=self.PORT
        )

    def _load(self):
        self.DATABASE = os.getenv('DB_DATABASE')
        self.HOST = os.getenv('DB_DOCKER_HOST')
        self.PORT = os.getenv('DB_DOCKER_PORT')
        self.USERNAME = os.getenv('DB_USER')
        self.PASSWORD = os.getenv('DB_PASSWORD')


