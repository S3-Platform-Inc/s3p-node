from dataclasses import dataclass
from datetime import datetime


@dataclass
class Source:
    id: int
    name: str
    config: dict
    sphere: str
    load_date: datetime
