from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


class Discount(Enum):
    """Discount enum."""

    NONE = auto()
    NORMAL = auto()
    MEMBER = auto()


@dataclass
class Product:
    """Product dataclass."""

    name: str
    hash: int
    base_price: Optional[float]
    price: float
    discount: Discount


def launch():
    """Quick launch for use in interactive shells."""
    from . import coop
    from . import selver
    from . import StoreRegistry
    StoreRegistry.update_stores()
