import io
from functools import lru_cache

import requests
from requests import RequestException

from s3p_sdk.types import S3PDocument
from src.s3p_node.task.bus import Bus
from src.s3p_node.task.module.base_module import BaseModule
from .web_driver import WebDriver


class ForbiddenError(RequestException):
    """Ошибка доступа"""
    ...


class DownloadDocumentsWithParserMethods(BaseModule):
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
                # Файла нет, нужно продолжать попытки скачать другие файлы.
                continue

    def safe(self, doc: S3PDocument) -> io.BytesIO:
        i_try = 0
        while i_try < self.MAX_TRY:
            try:
                content = self._io_content(doc.link)
                return content
            except ForbiddenError:
                self._cookies(doc.link)
            except Exception as e:
                self.logger.exception(e)
                raise FileNotFoundError('File of document was not found')
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

    def _upload_document(self, document: S3PDocument, data: io.BytesIO):
        res = self.bus.fileserver.upload_file(document, data)
        if res:
            local_link, load_date = res
            self.bus.documents.update(
                document,
                S3PDocument(
                    id=document.id,
                    title=document.title,
                    abstract=document.abstract,
                    text=document.text,
                    link=document.link,
                    storage=local_link,
                    other=document.other,
                    published=document.published,
                    loaded=load_date
                ))
        else:
            # Нужно предусмотреть ошибки и сохранить в локальное хранилище
            raise NotImplemented
