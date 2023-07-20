import urllib.request

from sources_parser_platform.types import SPP_document
from src.sources_parser_platform.bus import Bus
from src.sources_parser_platform.module.spp_module import SPP_module


class DownloadDocumentsWithDB(SPP_module):
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
                ...
        ...

    def __save(self):
        ...
