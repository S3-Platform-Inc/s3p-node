from src.sources_parser_platform.driver.dbBroker import Document, Source, document2cd
from src.sources_parser_platform.parser.content_document import Content_Document


class FilterOnlyNewDocumentWithDB:
    """
    Модуль для фильтрации документов по их новизне, вызывая все документы из базы данных.

    DRAFT: Это тестовый модуль. Предполагается, что модули не могут напрямую обращаться к драйверам.
    """

    def __new__(cls, source: Source, el: list[Content_Document], *args, **kwargs) -> list[Content_Document]:

        print(args)
        return FilterOnlyNewDocumentWithDB.__filter(FilterOnlyNewDocumentWithDB.__previous_documents(source), el)

    @staticmethod
    def __previous_documents(source: Source) -> list[Content_Document]:

        documents: list[Document] = Document.all_by_source_name(source.name)
        content_documents: list[Content_Document] = [document2cd(cd) for cd in documents]
        return content_documents

    @staticmethod
    def __filter(_previous_documents: list[Content_Document], _new_documents: list[Content_Document]) \
            -> list[Content_Document]:

        filtered: list[Content_Document] = []
        for cd in _new_documents:
            for pd in _previous_documents:
                if hash(cd) != hash(pd):
                    filtered.append(cd)
        return filtered
