from src.sources_parser_platform.types import SPP_document
from ..flow import Flow


class SPP_FE_documents(Flow):
    data: list[SPP_document]

    def __init__(self, documents: list[SPP_document]):
        super().__init__()
        self.data = documents
        ...

    def update(self, document, new_document):
        """
        Обновляет данные документа
        :param document:
        :_type document:
        :param new_document:
        :_type new_document:
        """
        self.data[self.data.index(document)] = new_document
