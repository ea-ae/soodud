from django.db import transaction
import logging
from concurrent import futures
from datetime import datetime
from typing import Generator, Callable, NamedTuple

from . import clustering  # noqa
from data import models
from data import text_analysis
from . import Discount
from . import Product


logger = logging.getLogger('app')


class StoreRegistry:
    """Manage store instances."""

    Store = NamedTuple('Store',
                       name=str,
                       entrypoint=Callable[[Generator[None, Product, None]], None],
                       model=models.Store)
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
        if name not in (store.name for store in cls.registry):  # do not add duplicate stores
            cls.registry.append(cls.Store(name, func, model))

    @classmethod
    def update_stores(cls):
        """Concurrently update all store products. Requests releases GIL."""
        with futures.ThreadPoolExecutor() as executor:  # alternatively: ProcessPoolExecutor
            tasks = executor.map(cls.update_store, cls.registry)
            for _ in tasks:
                pass

    @staticmethod
    def update_store(store: Store):
        """Update a store."""
        def save_prices() -> Generator[None, Product, None]:
            """Save the new prices."""
            while True:
                product = yield
                store_product, product_created = models.StoreProduct.objects.get_or_create(
                    store=store.model,
                    name=product.name,
                    hash=product.hash,
                    defaults={
                        'product': None,
                        'has_barcode': product.has_barcode
                    }
                )
                store_product.last_checked = datetime.now()

                price, price_created = models.Price.objects.get_or_create(
                    product=store_product,
                    base_price=product.base_price,
                    sale_price=None if product.discount == Discount.NONE else product.price,
                    members_only=product.discount == Discount.MEMBER
                )

                if price_created:  # price has changed, update
                    if not product_created:  # price update
                        update = (f'{store_product.name} {store_product.current_price.price} -> {price.price} '
                                  f'({store_product.current_price.discount} -> {price.discount})')
                        print(update)  # temp
                        logger.info(update)
                    price.save()
                    store_product.current_price = price
                else:  # should be redundant, somewhy isn't
                    store_product.current_price = price
                store_product.save()

        saver_gen = save_prices()
        next(saver_gen)
        store.entrypoint(saver_gen)

    @classmethod
    def match_stores(cls):
        """Find and update all store matches."""
        stores = [models.StoreProduct.objects.filter(store=store.model.id).values('id', 'name', 'hash', 'has_barcode')
                  for store in cls.registry]
        processed_stores = []
        for i, store in enumerate(stores):
            processed_store = text_analysis.prepare_store(store)
            print(f'Store \'{cls.registry[i].name}\' processed ({i + 1}/{len(stores)})')
            processed_stores.append((cls.registry[i].model.id, processed_store))
        cls.find_matches(processed_stores)

    @classmethod
    def find_matches(cls, processed_stores: list[tuple[int, list[text_analysis.Text]]]):
        """Find matches for processed store products."""
        analyser = clustering.Analyser(clustering.SingleLinkageMatcher(), 0.75)
        for store_id, store in processed_stores:
            for product in store:
                analyser.create_product(product.id, store_id, product.barcode, product.tokens, product.quantity)
        analyser.analyse()
        clusters = analyser.get_clusters()
        print('Saving products to database')

        with transaction.atomic():
            models.Product.objects.all().delete()  # migrating existing clusters is too much unnecessary work
            for cluster in clusters:
                cls.add_product(cluster.get_items())  # bulk creation is not viable

    @classmethod
    def add_product(cls, store_products: list[clustering.StoreProduct]) -> models.Product:
        """Save a product to database."""
        sp_models = []
        quantities = set()
        for sp in store_products:
            sp_model = models.StoreProduct.objects.only('name', 'product', 'store__name').get(id=sp.id)
            sp_models.append(sp_model)
            for quantity in sp.quantities:
                quantity = (quantity[0], quantity[1])
                quantities.add(quantity)

        # choose product with longest name, but deprioritize prisma (4) products due to truncation issues
        longest_name = sorted(sp_models, key=lambda x: len(x.name) if x.store.name != 'Prisma' else 0)[-1].name

        product = models.Product.objects.create(
            name=longest_name,  # todo: erase quantity data and place it separately
            quantity=list(quantities)
        )
        product.storeproduct_set.add(*sp_models)
        product.save()
        return product
