from typing import BinaryIO, Callable
from io import BytesIO

from pypdf import PdfReader
import magic
import docx
import pandas

from spp.types import SPP_document
from spp.task.bus import Bus
from spp.task.module.spp_module import SPP_module


class ExtractTextFromFile(SPP_module):
    """
    Модуль для извлечения текста из документов и занесения его в параметр SPP_document._text

    DRAFT: Это тестовый модуль.
    """

    _MIMETYPES = {
        "application/pdf": '.pdf',
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": '.docx',
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": '.xlsx',
    }

    # STORAGE = 'fileserver'
    STORAGE = 'localstorage'

    def __init__(self, bus: Bus):
        super().__init__(bus)

        self._MIMETYPES_methods: dict[str, Callable] = {
            '.pdf': self._extract_pdf,
            '.docx': self._extract_docx,
            '.xlsx': self._extract_xlsx,
        }

        for doc in self.bus.documents.data:
            self._safe_extract(doc)

    def _safe_extract(self, doc: SPP_document):
        # Это тестовая версия. Требуется унифицировать mimetypes методы для всего SPPApp

        try:
            with self._file(doc) as _file_stream:
                _mimetype = self._mimetype(_file_stream.read(2048))
                _file_stream.seek(0, 0)
                if _mimetype in self._MIMETYPES:
                    try:
                        text = self._MIMETYPES_methods.get(self._MIMETYPES.get(_mimetype))(_file_stream)
                        self._update_data_document(doc, text)
                    except Exception as e:
                        # Нужно ошибку обработки ошибки извлечения текста из файла
                        print(e)
                    ...
                else:

                    # Тоже ошибка. Файл не поддерживается. Нужно продолжить обработку, но запомнить это.
                    print(f'[ExtractTextFromFile] | ERROR: MIMETYPES не поддерживается | [{doc.doc_id}, {doc.title}]')
        except Exception as e:

            # В случае, если документ невозможно прочитать, просто продолжаем.
            print(f'[ExtractTextFromFile] | ERROR: File not exist | [{doc.doc_id}, {doc.title}]')
            ...
        ...

    def _file(self, doc: SPP_document) -> BinaryIO | BytesIO:
        if self.STORAGE == "fileserver":
            return self.bus.fileserver.file(doc)
        elif self.STORAGE == 'localstorage':
            return self.bus.local_storage.file(doc)
        # Нет способа получить файл
        raise NotImplemented

    def _mimetype(self, _bytes: bytes) -> str:
        """

        :param _bytes: Передаются первые 2048 байт файла для определения его типа
        :type _bytes:
        :return:
        :rtype:
        """
        return magic.from_buffer(_bytes, mime=True)

    def _update_data_document(self, doc: SPP_document, _text: str):
        self.bus.documents.update(
            doc,
            SPP_document(
                doc_id=doc.doc_id,
                title=doc.title,
                abstract=doc.abstract,
                text=_text,
                web_link=doc.web_link,
                local_link=doc.local_link,
                other_data=doc.other_data,
                pub_date=doc.pub_date,
                load_date=doc.load_date
            )
        )
        ...

    def _extract_pdf(self, _file: BinaryIO) -> str:
        reader = PdfReader(_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text

    def _extract_docx(self, _file: BinaryIO) -> str:
        __doc = docx.Document(_file)
        docText = '\n\n'.join(
            paragraph.text for paragraph in __doc.paragraphs
        )
        return docText

    def _extract_xlsx(self, _file: BinaryIO) -> str:
        df = pandas.read_excel(_file)
        t = '\n\n'.join([str(x) for x in df.values])
        return t
