"""Services."""
import itertools as it
import logging

from .stores import StoreRegistry


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    # from .stores import coop, selver, rimi
    from .stores import prisma
    StoreRegistry.update_stores()


def match():
    """Match products together."""
    from .stores import coop, selver, rimi, prisma
    StoreRegistry.match_stores()


def purge():
    """Purge Products with no associated StoreProducts, clear cache, etc."""
