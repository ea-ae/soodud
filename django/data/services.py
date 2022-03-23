"""Services."""


def launch():
    """Quick launch for use in interactive shells."""
    from .stores import StoreRegistry, coop, selver
    StoreRegistry.update_stores()
