from dataclasses import dataclass
from datetime import datetime

from .source import Source


@dataclass
class Document:
    doc_id: int
    title: str
    abstract: str
    text: str
    web_link: str
    local_link: str
    other_data: dict
    pub_date: datetime
    load_date: datetime
    source: Source
