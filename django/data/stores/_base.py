import hashlib
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional


class Discount(Enum):
    """Discount enum."""

    NONE = auto()
    NORMAL = auto()
    MEMBER = auto()

    def __str__(self):
        return self.name


@dataclass
class Product:
    """Product dataclass."""

    name: str
    base_price: Optional[float]
    price: float
    discount: Discount
    hash: str
    has_barcode: bool


def product_hash(store_name: str, data: int | str):
    """Form a store-dependent random hash for the product."""
    return str(int(hashlib.sha256(str.encode(f'{store_name}{data}')).hexdigest(), 16))[:-30:-1]
