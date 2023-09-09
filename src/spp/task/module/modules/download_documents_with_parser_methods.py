import io
from functools import lru_cache

import requests
from requests import RequestException

from spp.types import SPP_document
from spp.task.bus import Bus
from spp.task.module.spp_module import SPP_module
from .web_driver import WebDriver


class ForbiddenError(RequestException):
    """Ошибка доступа"""
    ...


class DownloadDocumentsWithParserMethods(SPP_module):
    """
    Модуль для скачивания документов, используя метод парсера для прохождения проверок и получения кук.
    При успешном скачивании, сохраняет файл в FTP сервер. Если есть необходимость,
    то сохраняет в локальное хранилище

    DRAFT: Это тестовый модуль.
    """

    MAX_TRY = 5
    TIMEOUT = 60
    cookies: list[dict] = []

    def __init__(self, bus: Bus):
        super().__init__(bus)
        self.download()
        ...

    @lru_cache()
    def _cookies(self, url):
        d = self.bus.entity('p_accept')(WebDriver(), url)
        self.cookies = d

    def download(self):
        for doc in self.bus.documents.data:
            try:
                with self.safe(doc) as data:
                    self._upload_document(doc, data)
            except FileNotFoundError as e:
                # Файла нет, нужно продолжать попытки скачать другие файлы.\
                continue

    def safe(self, doc: SPP_document) -> io.BytesIO:
        i_try = 0
        while i_try < self.MAX_TRY:
            try:
                content = self._io_content(doc.web_link)
                return content
            except ForbiddenError:
                self._cookies(doc.web_link)
            except Exception as e:
                print(e)
                raise FileNotFoundError('File of document was not found')
                # raise NotImplemented
            finally:
                i_try += 1
        raise FileNotFoundError('File of document was not found')

    def _io_content(self, url: str) -> io.BytesIO:
        cc = {}
        for cookie in self.cookies:
            cc[cookie['name']] = cookie['value']

        r = requests.get(url, cookies=cc, allow_redirects=False)
        if not r.ok:
            raise ForbiddenError('Any error without Response 200')
        return io.BytesIO(r.content)

    def _upload_document(self, document: SPP_document, data: io.BytesIO):
        res = self.bus.fileserver.upload_file(document, data)
        if res:
            local_link, load_date = res
            self.bus.documents.update(
                document,
                SPP_document(
                    doc_id=document.doc_id,
                    title=document.title,
                    abstract=document.abstract,
                    text=document.text,
                    web_link=document.web_link,
                    local_link=local_link,
                    other_data=document.other_data,
                    pub_date=document.pub_date,
                    load_date=load_date
                ))
        else:
            # Нужно предусмотреть ошибки и сохранить в локальное хранилище
            raise NotImplemented
