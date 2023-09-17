from __future__ import annotations

from logging import Logger, getLogger
from typing import TYPE_CHECKING
import multiprocessing

from spp.task.types.spp_parser_task import SPP_Parser_Task
from spp.plugin.abc_plugin import ABC_Plugin

if TYPE_CHECKING:
    from spp.types import SPP_plugin
    from src.spp.task import Task


class DynamicMultiprocessorTaskPool:
    """
    Core объект платформы.

    Динамический мультипроцессорный пул задач
    """

    _log: Logger
    _task_collection: dict[SPP_plugin, Task]
    _mp_pool: multiprocessing.Pool

    def __init__(self):
        self._log = getLogger()
        self._task_collection = {}

        self.mp_plugins = []
        self._mp_pool = multiprocessing.Pool()

    @property
    def count(self):
        """
        Количество всех задач
        :return:
        :rtype:
        """
        return len(self._task_collection)

    @property
    def active_count(self):
        """
        Количество всех активных задач
        :return:
        :rtype:
        """
        return len([task for task in self._task_collection.values() if task.is_alive()])

    @property
    def inactive_count(self):
        """
        Количество всех неактивных задач
        :return:
        :rtype:
        """
        return len([task for task in self._task_collection.values() if not task.is_alive()])

    def add(self, plugin: ABC_Plugin):
        self._plugin_is_instance(plugin)
        self._safe_exists(plugin)
        # Плагин с парсером
        new_task = SPP_Parser_Task(plugin)
        self._task_collection[plugin.metadata] = new_task
        self._log.debug(f'Task for spp_plugin {plugin.metadata.repository} has been added to pool')

    def tadd(self, plugin: ABC_Plugin):
        self._plugin_is_instance(plugin)
        if plugin.metadata in self.mp_plugins:
            self._log.exception(KeyError('This spp_plugin is already being processed'))
            raise KeyError('This spp_plugin is already being processed')

        new_task = SPP_Parser_Task(plugin)
        self._mp_pool.apply_async(new_task)
        self.mp_plugins.append(plugin)

    def pop(self, plugin: ABC_Plugin):
        self._plugin_is_instance(plugin)
        self._close_task(self._task_collection.get(plugin.metadata))
        self._task_collection.pop(plugin.metadata)
        self._log.debug(f'Task for spp_plugin {plugin.metadata.repository} has been deleted from pool')

    def start(self, plugin: ABC_Plugin):
        self._plugin_is_instance(plugin)
        try:
            self._log.debug(f'Task for spp_plugin {plugin.metadata.repository} has been started')
            task = self._task_collection.get(plugin.metadata)
            task.start()
        except KeyError as e:
            self._log.exception(e)
            raise e
        except RuntimeError as e:
            # Появляеться, если попытаться запустить заново одну задачу
            self._log.exception(e)
            raise e

    def stop(self, plugin: ABC_Plugin, hard: bool = False):
        self._plugin_is_instance(plugin)
        try:
            task = self._task_collection.get(plugin.metadata)
            if hard:
                task.terminate()
            else:
                task.join()
        except KeyError as e:
            self._log.exception(e)
            raise e
        except ValueError as e:
            # Поток задачи уже закрыт
            self._log.exception(e)
            raise e

    def is_finished(self, plugin: ABC_Plugin):
        self._plugin_is_instance(plugin)
        try:
            task = self._task_collection.get(plugin.metadata)
            return not task.is_alive()
        except KeyError as e:
            self._log.exception(e)
            raise e
        except ValueError as e:
            # Поток задачи уже закрыт
            self._log.exception(e)
            raise e

    def clear(self):
        """
        Удаляет из пула все неактивные задачи
        :return:
        :rtype:
        """
        plugins_for_delete = []

        for plugin in self._task_collection:
            task = self._task_collection.get(plugin)
            if not task.is_alive():
                self._close_task(task)
                plugins_for_delete.append(plugin)

        for plugin in plugins_for_delete:
            self._log.debug(f'Plugin {plugin.repository} has been deleted')
            del self._task_collection[plugin]

    def _close_task(self, task: Task):
        try:
            task.close()
        except ValueError as e:
            self._log.exception(e)
            task.terminate()
            task.close()

    def _plugin_is_instance(self, plugin: ABC_Plugin):
        if not isinstance(plugin, ABC_Plugin):
            self._log.exception(TypeError('spp_plugin must be a ABC_Plugin of type'))
            raise TypeError('spp_plugin must be a ABC_Plugin of type')

    def _safe_exists(self, plugin: ABC_Plugin):
        if plugin.metadata in self._task_collection:
            self._log.exception(KeyError('This spp_plugin is already being processed'))
            raise KeyError('This spp_plugin is already being processed')
