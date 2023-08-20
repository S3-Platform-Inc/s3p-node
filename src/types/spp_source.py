from dataclasses import dataclass
from datetime import datetime


@dataclass
class SPP_source:
    """
    Объект источника в SPP
    """
    src_id: int
    name: str
    config: dict
    sphere: str
    load_date: datetime
