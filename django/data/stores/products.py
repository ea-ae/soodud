"""Product formatting classes."""

from enum import Enum, auto


class Discount(Enum):
    """Discount enum."""

    NONE = auto()
    NORMAL = auto()
    MEMBER = auto()
