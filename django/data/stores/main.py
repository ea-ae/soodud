from concurrent import futures
from enum import Enum, auto
from typing import Callable, NamedTuple

import coop
import selver


class Discount(Enum):
    """Discount enum."""

    NONE = auto()
    NORMAL = auto()
    MEMBER = auto()


class StorePool:
    """Manage store instances."""

    Store = NamedTuple('Store', name=str, entrypoint=Callable)

    def __init__(self):
        """Initialize."""
        self.registry: list[StorePool.Store] = []

    def add_store(self, name: str, func: Callable):
        """Add store to registry."""
        self.registry.append(StorePool.Store(name, func))

    def update_all(self):
        """Concurrently update all stores. Requests releases GIL."""
        with futures.ThreadPoolExecutor() as executor:  # alternatively: ProcessPoolExecutor
            tasks = executor.map(self.update_store, self.registry)
            for _ in tasks:
                pass

    @staticmethod
    def update_store(store: Store):
        """Update a store."""
        def save_prices(x: int):
            """Save the new prices."""
            print(f'{store.name} returned {x}')
        store.entrypoint(save_prices)


if __name__ == '__main__':
    stores = StorePool()
    stores.add_store('Coop', coop.main)  # decorators don't work here
    stores.add_store('Selver', selver.main)
    stores.update_all()
