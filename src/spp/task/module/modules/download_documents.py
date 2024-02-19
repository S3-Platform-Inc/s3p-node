import urllib.request

from src.spp.types import SPP_document
from src.spp.task.bus import Bus
from src.spp.task.module.spp_module import SppModule


class DownloadDocumentsWithDB(SppModule):
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

        ...

    def __download(self, document: SPP_document, link: str):
        with urllib.request.urlopen(link) as f:
            res = self.bus.fileserver.upload_file(document, f)
            if res:
                local_link, load_date = res
                self.bus.documents.update(
                    document,
                    SPP_document(
                        id=document.id,
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
                ...
        ...

    def __save(self):
        ...
