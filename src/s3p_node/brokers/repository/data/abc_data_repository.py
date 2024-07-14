from __future__ import annotations

import io
from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, BinaryIO

if TYPE_CHECKING:
    from s3p_sdk.types import S3PDocument, S3PRefer


class AbcDataRepository(metaclass=ABCMeta):
    """
    Абстрактный класс репозитория с данными
    """

    _reference: S3PRefer  # Объект связки для сохранения файлов в репозитории

    @abstractmethod
    def file(self, document: S3PDocument) -> io.BytesIO:
        """
        Получение файла из репозитория
        """
        ...

    @abstractmethod
    def rename(self, document: S3PDocument, new_filename: str) -> str | Exception:
        """
        Переименование файла в репозитории
        :param document:
        :param new_filename:
        :return:
        """
        ...

    @abstractmethod
    def delete(self, document: S3PDocument) -> io.BytesIO:
        """
        Удаление документа в репозитории.
        Стоит задуматься над необходимостью удаления загруженного документа
        :param document:
        :return:
        """

    @abstractmethod
    def save(self, document: S3PDocument, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Сохраняет документ в репозитории
        :param document:
        :param data:
        :return:
        """
        ...

    @abstractmethod
    def update(self, document: S3PDocument, data: bytes | io.BytesIO | BinaryIO) -> str | Exception:
        """
        Обновляет документ в репозитории
        :param document:
        :param data:
        :return:
        """
        ...

    ...
