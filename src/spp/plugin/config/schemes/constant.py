from dataclasses import dataclass


@dataclass
class ConstantObject:
    """
    Объект, представляющий константу
    """
    value: object
