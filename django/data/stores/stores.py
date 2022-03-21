from concurrent import futures
from datetime import datetime
from typing import Generator, Callable, NamedTuple

from data import models
from data.stores.products import Discount, Product
from data.stores import coop
from data.stores import selver


class StorePool:
    """Manage store instances."""

    Store = NamedTuple('Store', name=str, entrypoint=Callable, model=models.Store)

    def __init__(self):
        """Initialize."""
        self.registry: list[StorePool.Store] = []

    def add_store(self, name: str, func: Callable):
        """Add store to registry."""
        model, created = models.Store.objects.get_or_create(name=name)
        self.registry.append(StorePool.Store(name, func, model))

    def update_all(self):
        """Concurrently update all stores. Requests releases GIL."""
        with futures.ThreadPoolExecutor() as executor:  # alternatively: ProcessPoolExecutor
            tasks = executor.map(self.update_store, self.registry)
            for _ in tasks:
                pass

    @staticmethod
    def update_store(store: Store):
        """Update a store."""
        def save_prices(x: int) -> Generator[None, Product, None]:
            """Save the new prices."""
            while True:
                product = yield
                print(f'{store.name} returned with {product}')

                store_product, _ = models.StoreProduct.objects.get_or_create(  # leave Product as null for now!
                    store=store.model,
                    name=product.name,
                    defaults={
                        'product': None
                    }
                )
                store_product.last_checked = datetime.now()
                store_product.save()
                price, created = models.Price.objects.get_or_create(
                    product=store_product,
                    current=True,
                    defaults={
                        'base_price': product.base_price,
                        'sale_price': product.price,
                        'members_only': product.discount == Discount.MEMBER
                    }
                )
                if not created:
                    stored_prices = (price.base_price, price.sale_price, price.members_only)
                    new_prices = (product.base_price, product.price, product.discount == Discount.MEMBER)
                    if stored_prices != new_prices:  # prices changed
                        price.current = False
                        price.save()
                        new_price = models.Price(
                            product=store_product,
                            current=True,
                            base_price=new_prices[0],
                            sale_price=new_prices[1],
                            members_only=new_prices[2]
                        )
                        new_price.save()

        store.entrypoint(save_prices)


if __name__ == '__main__':
    stores = StorePool()
    stores.add_store('Coop', coop.main)  # decorators don't work here
    # stores.add_store('Selver', selver.main)
    stores.update_all()
