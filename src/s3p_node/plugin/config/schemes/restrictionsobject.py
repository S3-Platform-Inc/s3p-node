from dataclasses import dataclass
from datetime import datetime


@dataclass
class RestrictionsObject:
    """
    Класс, представляющий конфигурацию ограничений для плагина.

    Attributes:
        maximum_materials (int | None): Максимальное количество материалов для сбора.
            Если None, ограничение не применяется.
        to_last_material (bool | None): Флаг, указывающий, нужно ли собирать материалы
            до последнего известного материала. Если True, сбор прекращается при
            достижении последнего известного материала.
        from_date (datetime | None): Дата и время начала периода сбора материалов.
            Если None, нижняя граница периода не устанавливается.
        to_date (datetime | None): Дата и время окончания периода сбора материалов.
            Если None, верхняя граница периода не устанавливается.

    Этот класс используется для задания параметров ограничения при сборе материалов,
    позволяя контролировать количество собираемых материалов и временной диапазон сбора.
    """
    maximum_materials: int | None
    to_last_material: bool | None
    from_date: datetime | None
    to_date: datetime | None
