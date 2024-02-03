import datetime
import io
from ftplib import FTP
from hashlib import sha224
from typing import BinaryIO

from .setting import setting
from src.spp.types import SPP_source, SPP_document


class SPP_file_server_broker:
    __source: SPP_source

    def __init__(self, src: SPP_source):
        self.__source = src
        ...

    def upload_document(self, document: SPP_document, bin_doc: bytes | io.BytesIO | BinaryIO) -> bool | str:
        """
        Метод загружает на FTP сервер документ
        :param document:
        :_type document:
        :param bin_doc:
        :_type bin_doc:
        :return:
        :rtype:
        """

        # Красивое применение парадигмы Elegant Objects. Уххх (^///^)
        local_link = ""
        binaryfile = io.BytesIO(bin_doc) if isinstance(bin_doc, bytes) else bin_doc
        try:
            local_link, session = self.__safe_upload(
                self.__safe_source_dir(
                    self.__work_dir(
                        self.__session()
                    )
                ), document, binaryfile
            )
            session.close()
        except Exception as e:
            return False

            # Надо решить что делать в случае ошибки
            raise NotImplemented
        else:
            return local_link

    def document(self, document: SPP_document) -> io.BytesIO:
        """
        Метод для получения файлв документа по объекту SPP_document
        :param document:
        :type document:
        :return:
        :rtype:
        """

        return self._safe_download(
            self.__safe_source_dir(
                self.__work_dir(
                    self.__session()
                )
            ), document
        )

    def _safe_download(self, sourced_session: FTP, doc: SPP_document) -> io.BytesIO:
        try:
            _bytes_stream = io.BytesIO()
            if doc.local_link:
                sourced_session.retrbinary(f"RETR {doc.local_link}", _bytes_stream.write)
                _bytes_stream.seek(0, 0)
            else:
                sourced_session.retrbinary(f"RETR {self.__document_filename(doc)}", _bytes_stream.write)
            return _bytes_stream
        except Exception as e:
            # Нужна ошибка файла в файловом сервере
            raise NotImplemented

    def __safe_upload(self, session: FTP, doc: SPP_document, binaryfile: io.BytesIO | BinaryIO) -> tuple[str, FTP]:
        try:
            int_pad = 0
            pad = ''
            while self.__exist_file(session, self.__document_filename(doc, pad)):
                # Вообще - это ненормально поведение. если мы решили сохранять файл, то его название не может повториться
                int_pad += 1
                pad = str(int_pad)

            session.storbinary("STOR " + self.__document_filename(doc, pad), binaryfile, setting.BLOCKSIZE)
            local_link = session.pwd() + '/' + self.__document_filename(doc, pad)
            return local_link, session
        except Exception as e:
            # Реализовать обработку исключения
            raise NotImplemented

    def __upload(self, session: FTP, doc: SPP_document, binaryfile: io.BytesIO) -> FTP:
        try:
            session.storbinary("STOR " + self.__document_filename(doc), binaryfile, setting.BLOCKSIZE)
        except Exception as e:
            # Ошибка отправки
            raise NotImplemented
        else:
            return session

    def __safe_source_dir(self, session: FTP) -> FTP:
        """
        Безопасно возвращает сессию с директорией источника.
        Если таковой нет, то создает ее.
        :param session: Сессия в рабочей директории
        :_type session:
        :return:
        :rtype:
        """
        if not self.__exist_dir(session, self.__sourced_dirname()):
            # Необходимо создать директорию, перейти в нее и вернуть сессию
            session.mkd(self.__sourced_dirname())

        # Переходим в нее и возвращаем сессию
        session.cwd(self.__sourced_dirname())
        return session

    def __session(self) -> FTP:
        try:
            ftp = FTP(setting.PASSV_ADDR)
            print(ftp.login(setting.FTP_USER, setting.FTP_PASS))
        except ConnectionRefusedError as e:
            # Ошибка соединения
            raise NotImplemented
        except Exception as e:
            # Нужно сделать так, чтобы ошибка подключения
            raise NotImplemented
        return ftp

    def __work_dir(self, session: FTP) -> FTP:
        print(session.cwd(setting.WORK_DIR))
        return session

    def __sourced_dirname(self) -> str:
        """
        Генерирует Hash из названия источника. Уникальное имя для директории
        :return: Hash название директории источника
        :rtype:
        """
        return str(sha224(self.__source.name.encode('utf8')).hexdigest())

    def __document_filename(self, doc: SPP_document, pad: str = "") -> str:
        concat_name = doc.title + '_' + doc.web_link + '_' + str(doc.pub_date.timestamp())

        return str(
            sha224(concat_name.encode('utf8')).hexdigest()) + f"_{doc.title}_{str(doc.pub_date.timestamp())}_({pad})"

    def __exist_dir(self, dir_session: FTP, dirname: str) -> bool:
        return dirname in list(dir_session.nlst())

    def __exist_file(self, session: FTP, filename: str) -> bool:
        return filename in list(session.nlst())

    def test(self):

        print(self.__exist_dir(self.__work_dir(self.__session()), self.__source.name))


if __name__ == "__main__":
    fs = SPP_file_server_broker(SPP_source(3, 'r3r', {}, '', datetime.datetime.now()))
    dt = datetime.datetime.now()
    d = b'PNG?> test document PNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test documentPNG?> test document'
    fs.upload_document(SPP_document(1, '1', '2', '3', '4', '5', {}, dt, dt), d)
