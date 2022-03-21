from concurrent import futures
from typing import Generator, Callable, NamedTuple

from products import ProductData
import coop
import selver


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
        def save_prices(x: int) -> Generator[None, ProductData, None]:
            """Save the new prices."""
            while True:
                y = yield
                print(f'{store.name} returned {x} with {y}')
        store.entrypoint(save_prices)


if __name__ == '__main__':
    stores = StorePool()
    stores.add_store('Coop', coop.main)  # decorators don't work here
    # stores.add_store('Selver', selver.main)
    stores.update_all()
