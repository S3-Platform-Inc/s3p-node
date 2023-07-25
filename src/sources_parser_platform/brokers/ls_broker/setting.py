import os
from dataclasses import dataclass


@dataclass
class Control:
    documents: dict

    def add(self, _hash: bytes, filename: str):
        """
        Добавляет связь hash документа и имя скачанного файла
        :param _hash:
        :_type _hash:
        :param filename:
        :_type filename:
        """
        self.documents[_hash] = filename


@dataclass
class Setting:
    # WORK_DIR: str = 'spp\\sources'
    # CONTROL_FILE: str = '.control.temp.pkl'

    WORK_DIR: str = os.environ.get('LS_WORK_DIR')
    CONTROL_FILE: str = os.environ.get('LS_CONTROL_FILENAME')
    DEFAULT_CONTROL = Control({})


setting = Setting()
