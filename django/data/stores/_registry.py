from concurrent import futures
from datetime import datetime
from typing import Generator, Callable, NamedTuple

from data import models
from . import Discount
from . import Product


class StoreRegistry:
    """Manage store instances."""

    Store = NamedTuple('Store', name=str, entrypoint=Callable, model=models.Store)
    registry: list[Store] = []

    def __init__(self, name: str):
        """Initialize."""
        self.store_name = name

    def __call__(self, func: Callable):
        """Called by decorators."""
        self.add_store(self.store_name, func)

    @classmethod
    def add_store(cls, name: str, func: Callable):
        """Add store to registry."""
        model, _ = models.Store.objects.get_or_create(name=name)
        cls.registry.append(cls.Store(name, func, model))

    @classmethod
    def update_stores(cls):
        """Concurrently update all stores. Requests releases GIL."""
        with futures.ThreadPoolExecutor() as executor:  # alternatively: ProcessPoolExecutor
            tasks = executor.map(cls.update_store, cls.registry)
            for _ in tasks:
                pass

    @staticmethod
    def update_store(store: Store):
        """Update a store."""
        def save_prices(x: int) -> Generator[None, Product, None]:
            """Save the new prices."""
            while True:
                product = yield
                # print(f'{store.name} returned with {product}')

                store_product, _ = models.StoreProduct.objects.get_or_create(  # leave Product as null for now!
                    store=store.model,
                    name=product.name,
                    hash=product.hash,
                    defaults={
                        'product': None,
                        'has_barcode': product.has_barcode
                    }
                )
                store_product.last_checked = datetime.now()

                price, created = models.Price.objects.get_or_create(
                    product=store_product,
                    base_price=product.base_price,
                    sale_price=None if product.discount == Discount.NONE else product.price,
                    members_only=product.discount == Discount.MEMBER
                )
                if created:  # price has changed, update
                    price.save()
                    store_product.current_price = price
                store_product.save()

        store.entrypoint(save_prices)
