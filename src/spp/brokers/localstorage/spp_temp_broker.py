import os
import pickle
from hashlib import sha224
from typing import BinaryIO

from src.spp.types import SPP_source, SPP_document
from .setting import setting, Control


class SPP_temp_broker:
    __source: SPP_source
    __base_path: str
    __control: Control

    def __init__(self, src: SPP_source, local_path: str):
        self.__source = src
        self.__base_path = local_path

        self._check_directory(self.work_dir)
        try:
            self._check_directory(self.source_dir)
        except NotADirectoryError:
            os.mkdir(self.source_dir)
        self._pre_load_control_file()

    @property
    def work_dir(self) -> str:
        """
        Свойство для получения полного пути до рабочего каталога
        :return:
        :rtype:
        """
        return os.path.join(self.__base_path, setting.WORK_DIR)

    @property
    def source_dir(self) -> str:
        """
        Свойство для получения полного пути до директории источника
        :return:
        :rtype:
        """
        return os.path.join(self.work_dir, self.__source.name)

    def _sourced_file_path(self, file: str) -> str:
        return os.path.join(self.source_dir, file)

    @staticmethod
    def _check_directory(path: str):
        if not os.path.isdir(path):
            raise NotADirectoryError(f"{path} can't destinations")

    def _pre_load_control_file(self):
        file_list = os.listdir(self.source_dir)
        if setting.CONTROL_FILE in file_list:
            # Файл существует
            self.__control = pickle.load(open(self._sourced_file_path(setting.CONTROL_FILE), 'rb'))
        else:
            # Файл не найден. Требуется создать
            self.__control = setting.DEFAULT_CONTROL
            self._save_control_file()

    def _save_control_file(self):
        # Требуется обязательно сохранять файл контроля после изменения
        pickle.dump(self.__control, open(self._sourced_file_path(setting.CONTROL_FILE), 'wb'))

    def __document_filename(self, doc: SPP_document) -> str:
        concat_name = doc.title + '_' + doc.web_link + '_' + str(doc.pub_date.timestamp())

        return str(sha224(concat_name.encode('utf8')).hexdigest())

    def file(self, doc: SPP_document) -> BinaryIO:
        filename = self.__control.documents.get(doc.hash)
        return open(self._sourced_file_path(filename), 'rb')

    def link(self, document: SPP_document, filename) -> bool:
        if not self.__control.documents.get(document.hash, False):
            if not os.path.isfile(self._sourced_file_path(filename)):
                raise FileNotFoundError(filename)
            self.__control.add(document.hash, filename)
            self._save_control_file()
            return True
        else:
            return False

    def rename(self, document: SPP_document, name: str = ''):
        old_filename = self.__control.documents.get(document.hash)
        if not name:
            name = old_filename + '_' + self.__document_filename(document)

        if os.path.isfile(self._sourced_file_path(old_filename)):
            os.rename(self._sourced_file_path(old_filename), self._sourced_file_path(name))
            self.__control.documents[document.hash] = name
            self._save_control_file()
        else:
            ...
