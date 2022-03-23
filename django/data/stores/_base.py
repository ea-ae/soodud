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
    base_price: Optional[float]
    price: float
    discount: Discount
    hash: int
    has_barcode: bool
