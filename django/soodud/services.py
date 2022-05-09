"""Services."""

from django.core.cache import cache

from api.views import ProductViewSet
from data.stores import StoreRegistry


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    from data.stores import coop, selver, rimi, prisma
    StoreRegistry.update_stores()


def match():
    """Match products together."""
    from data.stores import coop, selver, rimi, prisma
    StoreRegistry.match_stores()
    purge()


def purge():
    """Purge Products with no associated StoreProducts, clear cache, etc."""
    cache.clear()


def load_cache():
    """Create a product cache."""
    ProductViewSet.create_cache()
