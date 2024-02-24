from __future__ import annotations

import io
import logging
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, BinaryIO

if TYPE_CHECKING:
    from src.spp.plugin.abc_plugin import AbcPlugin
    from src.spp.types import SppTask, SPP_document, SppRefer


class AbcDataRepository(metaclass=ABCMeta):
    """
    Абстрактный класс репозитория с данными
    """

    _reference: SppRefer  # Объект связки для сохранения файлов в репозитории

    @abstractmethod
    def file(self, document: SPP_document) -> io.BytesIO:
        """
        Получение файла из репозитория
        """
        ...

    @abstractmethod
    def rename(self, document: SPP_document, new_filename: str) -> str | Exception:
        """
        Переименование файла в репозитории
        :param document:
        :param new_filename:
        :return:
        """
        ...

    @abstractmethod
    def delete(self, document: SPP_document) -> io.BytesIO:
        """
        Удаление документа в репозитории.
        Стоит задуматься над необходимостью удаления загруженного документа
        :param document:
        :return:
        """

    @abstractmethod
    def save(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Сохраняет документ в репозитории
        :param document:
        :param data:
        :return:
        """
        ...

    @abstractmethod
    def update(self, document: SPP_document, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Обновляет документ в репозитории
        :param document:
        :param data:
        :return:
        """
        ...

    ...
