"""Services."""
import itertools as it
import logging

from data.stores import StoreRegistry
from api.views import ProductViewSet


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    from data.stores import coop, selver, rimi, prisma
    StoreRegistry.update_stores()


def match():
    """Match products together."""
    from data.stores import coop, selver, rimi, prisma
    StoreRegistry.match_stores()


def purge():
    """Purge Products with no associated StoreProducts, clear cache, etc."""


def load_cache():
    """Create a product cache."""
    ProductViewSet.create_cache()
