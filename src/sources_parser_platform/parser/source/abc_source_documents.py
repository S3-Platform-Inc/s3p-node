from abc import ABCMeta
from typing import List

from sources_parser_platform.parser.content_document import Content_Document


class ABC_Source_Document(metaclass=ABCMeta):

    def content(self, category_type: str, subcategory_type: str) -> List[Content_Document]: ...

    def _parse(self): ...
