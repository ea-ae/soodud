"""Services."""
import itertools as it

from .stores import StoreRegistry


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    from .stores import rimi
    StoreRegistry.update_stores()


def match():
    """Match products together."""
    from .stores import coop, selver, rimi
    StoreRegistry.match_stores()
