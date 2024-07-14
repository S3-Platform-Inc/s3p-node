import os
import pickle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from s3p_sdk.types import S3PDocument


class ControlFile:

    def __init__(self, work_directory: str):
        self.work_directory = work_directory
        self._documents: dict[bytes, str] = {}
        self.CONTROL_FILE: str = os.environ.get('LS_CONTROL_FILENAME')

    def filename(self, document: S3PDocument) -> str | Exception:
        """
        Имя файла документа в локальном хранилище
        :param document:
        :return:
        """
        if document.hash in self._documents.keys():
            return self._documents.get(document.hash)
        else:
            KeyError(f'Document {document.id}, {document.title}, {document.hash} not found in control file')

    def add(self, document: S3PDocument, filename: str):
        """
        Добавляет связку SppDocument --> filename of document
        :param document:
        :param filename:
        :return:
        """
        if document.hash in self._documents.keys():
            raise KeyError(f'Document {document.id}, {document.title}, {document.hash} already in control file')

        self._documents[document.hash] = filename

    def rename(self, document: S3PDocument, new_filename: str):
        """
        Изменяет имя файла документа
        :param document:
        :param new_filename:
        :return:
        """
        if document.hash not in self._documents.keys():
            raise KeyError(f'Document {document.id}, {document.title}, {document.hash} not found in control file')

        self._documents[document.hash] = new_filename

    def _preload(self):
        if self.CONTROL_FILE in os.listdir(self.work_directory):
            # Файл существует
            self._documents = pickle.load(open(self._path(), 'rb'))
        else:
            # Файл не найден. Требуется создать
            self.__control = {}
            self._save()

    def _save(self):
        pickle.dump(self.__control, open(self._path(), 'wb'))

    def _path(self) -> str:
        return os.path.join(self.work_directory, self.CONTROL_FILE)
