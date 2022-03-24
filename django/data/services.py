"""Services."""
import itertools as it

from .stores import StoreRegistry
from .models import Store, Product, StoreProduct
from . import text_analysis


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    from .stores import coop, selver, rimi
    StoreRegistry.update_stores()


def match(*, size=500_000, start_offset=0):
    """Match products together."""
    stores = [StoreProduct.objects.filter(store=store.id).values('id', 'name')
              for store in Store.objects.only('id').all()]
    _match_stores(*stores)


def _match_stores(*args):
    """Find matches between two stores. TODO 3+ store clusters."""
    groups = []
    for i, store in enumerate(args):
        processed_store = text_analysis.prepare_store(store)
        print(f'Store processed ({i + 1}/{len(args)})')
        groups.append(processed_store)

    for match in text_analysis.find_matches(groups):
        a = StoreProduct.objects.only('name', 'product').get(id=match.id_a)
        b = StoreProduct.objects.only('name', 'product').get(id=match.id_b)

        if None not in (a.product_id, b.product_id) and a.product_id != b.product_id:
            # items in two separate clusters matched, merge them
            print('Merging product clusters', a.product_id, b.product_id)
            cluster_products = []  # get all products from clusters
            for product in (StoreProduct.objects.filter(product=p) for p in (a.product, b.product)):
                cluster_products.append(product)
            cluster_products.sort(key=lambda p: p.name, reverse=True)  # prioritize shorter names

            for product in (a.product, b.product):  # delete the two old clusters
                product.delete()

            obj, created = Product.objects.get_or_create(  # create a merged cluster
                name=cluster_products[0].name,
                quantity='todo',
                certainty=match.score
            )
            assert created  # must be new as the previous clusters were deleted
            obj.save()
            for product in cluster_products:  # assign StoreProducts from both clusters to the new Product
                product.product = obj
                product.save()

        product = a.product if a.product_id is not None else None
        product = b.product if product is None else product

        if product is None:  # neither match is already attached to a product (in cluster)
            obj, created = Product.objects.get_or_create(
                name=sorted((a.name, b.name))[-1],
                quantity='todo',
                certainty=match.score
            )
            assert created  # the object may already exist elsewhere in case we are dealing with two new StoreProducts
            obj.save()
            a.product, b.product = obj, obj
            a.save()
            b.save()
        else:
            for one, two in ((a, b), (b, a)):
                if one.product_id is None:
                    one.product = two.product


# def _match_product_set(limit: int, offset: int) -> int:
#     """Match a set of products with a limit and offset."""
#     matches = StoreProduct.objects.raw(
#         f'''
#         SELECT *
#         FROM (
#             SELECT sp.id AS id, sp.name AS name,
#             FROM data_storeproduct sp
#             WHERE
#           ) sp
#           INNER JOIN data_storeproduct sp2 ON (
#             AND sp.id < sp2.id
#             AND sp.store_id <> sp2.store_id
#             AND (sp.has_barcode = FALSE OR sp2.has_barcode = FALSE)
#           )
#         OFFSET {offset} ROWS FETCH NEXT
#         ''')
#     text_analysis.prepare()
