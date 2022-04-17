from concurrent import futures
from datetime import datetime
from typing import Generator, Callable, NamedTuple

from . import clustering  # noqa
from data import models
from data import text_analysis
from . import Discount
from . import Product


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
                        print(f'{store_product.name} {store_product.current_price.price} -> {price.price} '
                              f'({store_product.current_price.discount} -> {price.discount})')
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
        stores = [models.StoreProduct.objects.filter(store=store.model.id).values('id', 'name')
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
        analyser = clustering.Analyser(clustering.SingleLinkageMatcher(), 0.8)
        for store_id, store in processed_stores:
            for product in store:
                analyser.create_product(product.id, store_id, product.tokens, product.quantity)
        analyser.analyse()
        clusters = analyser.get_clusters()
        print('Saving products to database')

        #  migrating existing clusters is too much unnecessary work
        # in the future consider a smoother process where table is updated only at the end
        models.Product.objects.all().delete()

        for cluster in clusters:
            cls.add_product(cluster.get_items())

    @classmethod
    def add_product(cls, store_products: list[clustering.StoreProduct]):
        """Save a product to database."""
        sp_models = [models.StoreProduct.objects.only('name', 'product').get(id=sp.id) for sp in store_products]

        longest_name = sorted((sp.name for sp in sp_models), key=lambda x: len(x))[-1]
        product = models.Product.objects.create(
            name=longest_name,  # todo: erase quantity data and place it separately
            quantity='todo'
        )

        product.storeproduct_set.add(*sp_models)
        product.save()

    @classmethod
    def find_matches_old(cls, processed_stores: list[list[text_analysis.Text]]):
        """Old Python code for finding matches."""
        for match in text_analysis.find_matches(processed_stores):
            a = models.StoreProduct.objects.only('name', 'product').get(id=match.id_a)
            b = models.StoreProduct.objects.only('name', 'product').get(id=match.id_b)

            if None not in (a.product_id, b.product_id) and a.product_id != b.product_id:
                print('Merging product clusters', a.product_id, b.product_id, match)
                cls._merge_products(a, b, match.score)
                continue

            product = a.product if a.product_id is not None else None
            product = b.product if product is None else product

            if product is None:  # neither match is already attached to a product (in cluster)
                obj, created = models.Product.objects.get_or_create(
                    name=sorted((a.name, b.name), key=lambda x: len(x))[-1],
                    quantity='todo',
                    defaults={'certainty': match.score})
                if not created:
                    print('notcreated>', a.name, b.name, a.product, b.product, obj)
                a.product, b.product = obj, obj
                a.save()
                b.save()
            else:
                product.certainty = min(product.certainty, round(match.score, 2))
                product.save()
                for one, two in ((a, b), (b, a)):
                    if one.product_id is None:
                        one.product = two.product
                        one.save()

    @staticmethod
    def _merge_products(a: models.StoreProduct, b: models.StoreProduct, match_score: float):
        """Merge two clusters of store products into a new Product or multiple Products."""
        cluster_products = []  # get all products from clusters
        for cluster in (models.StoreProduct.objects.filter(product=p) for p in (a.product, b.product)):
            for cluster_product in cluster:
                cluster_products.append(cluster_product)

        # todo: if merged clusters contain same store products, don't merge all
        cluster_products.sort(key=lambda p: len(p.name), reverse=True)  # prioritize shorter names

        for product in (a.product, b.product):  # delete the two old clusters
            product.delete()

        print(cluster_products, a.product_id, b.product_id)

        obj, created = models.Product.objects.get_or_create(  # create a merged cluster
            name=cluster_products[0].name,
            quantity='todo',
            defaults={'certainty': match_score})
        assert created  # must be new as the previous clusters were deleted
        for product in cluster_products:  # assign StoreProducts from both clusters to the new Product
            product.product = obj
            product.save()
