import urllib.request

from s3p_sdk.types import S3PDocument
from src.s3p_node.task.module.base_module import BaseModule
from src.s3p_node.task.bus import Bus


class DownloadDocumentsWithDB(BaseModule):
    """
    Модуль для скачивания документов. При успешном скачивании, сохраняет файл в FTP сервер. Если есть необходимость,
    то сохраняет в локальное хранилище

    DRAFT: Это тестовый модуль.
    """

    __options = {
        'save:': (
            'fileserver',
            'local',
            'local+fileserver',
        ),
    }

    def __init__(self, bus: Bus):
        super().__init__(bus)

    def __download(self, document: S3PDocument, link: str):
        with urllib.request.urlopen(link) as f:
            res = self.bus.fileserver.upload_file(document, f)
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
                ...
        ...

    def __save(self):
        ...
