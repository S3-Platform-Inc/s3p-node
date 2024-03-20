from dataclasses import dataclass


@dataclass
class SppNode:
    """
    Структура узла платформы.
    """
    id: int | None
    name: str
    ip: str | None
    config: dict
    session: int | None
