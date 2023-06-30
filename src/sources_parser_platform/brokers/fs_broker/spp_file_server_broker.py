import datetime
import io
from ftplib import FTP
from hashlib import sha224

from .setting import setting
from ...types import SPP_source, SPP_document


class SPP_file_server_broker:
    __source: SPP_source

    def __init__(self, src: SPP_source):
        self.__source = src
        ...

    def upload_document(self, document: SPP_document, bin_doc: bytes) -> bool | str:
        """
        Метод загружает на FTP сервер документ
        :param document:
        :type document:
        :param bin_doc:
        :type bin_doc:
        :return:
        :rtype:
        """

        # Красивое применение парадигмы Elegant Objects. Уххх (^///^)
        local_link = ""
        binaryfile = io.BytesIO(bin_doc) if isinstance(bin_doc, bytes) else bin_doc
        try:
            self.__safe_upload(
                self.__safe_source_dir(
                    self.__work_dir(
                        self.__session()
                    )
                ), document, binaryfile, local_link
            ).close()
        except Exception as e:
            return False

            # Надо решить что делать в случае ошибки
            raise NotImplemented
        else:
            return local_link

    def __safe_upload(self, session: FTP, doc: SPP_document, binaryfile: io.BytesIO, path: str) -> FTP:
        try:
            doc_name = self.__document_filename(doc)
            int_pad = 0
            pad = ''

            while self.__exist_file(session, self.__document_filename(doc, pad)):
                # Вообще - это ненормально поведение. если мы решили сохранять файл, то его название не может повториться
                int_pad += 1
                pad = str(int_pad)

            session.storbinary("STOR " + self.__document_filename(doc, pad), binaryfile, setting.BLOCKSIZE)
            path = session.pwd() + '/' + self.__document_filename(doc, pad)
        except Exception as e:
            raise NotImplemented
        else:
            return session

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
        :type session:
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
            ftp.login(setting.FTP_USER, setting.FTP_PASS)
        except ConnectionRefusedError as e:
            # Ошибка соединения
            raise NotImplemented
        except Exception as e:
            # Нужно сделать так, чтобы ошибка подключения
            raise NotImplemented
        return ftp

    def __work_dir(self, session: FTP) -> FTP:
        session.cwd(setting.USER_DIR + setting.WORK_DIR)
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
