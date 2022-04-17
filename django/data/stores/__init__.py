"""Stores."""

from ._base import Discount
from ._base import Product
from ._base import product_hash
from ._registry import StoreRegistry


__all__ = ['Discount', 'Product', 'product_hash', 'StoreRegistry', 'coop', 'selver', 'prisma', 'rimi']
