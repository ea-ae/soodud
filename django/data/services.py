"""Services."""
import itertools as it

from .stores import StoreRegistry
from .models import Store, Product, StoreProduct
from . import text_analysis


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    from .stores import rimi
    StoreRegistry.update_stores()


def match(*, size=500_000, start_offset=0):
    """Match products together."""
    _match_stores(
        StoreProduct.objects.filter(store=1).values('id', 'name'),
        StoreProduct.objects.filter(store=2).values('id', 'name')
    )


def _match_stores(*args):
    """Find matches between two stores. TODO 3+ store clusters."""
    groups = []
    for store in args:
        # print(store, 'M<<')
        processed_store = text_analysis.prepare_store(store)
        # print(processed_store)
        print('Store processed!')
        groups.append(processed_store)

    matches = text_analysis.find_clusters(groups)
    for match in matches:
        # print(match.score,
        #       StoreProduct.objects.get(id=match.id_a).name,
        #       StoreProduct.objects.get(id=match.id_b).name)
        a = StoreProduct.objects.only('name', 'product').get(id=match.id_a)
        b = StoreProduct.objects.only('name', 'product').get(id=match.id_b)
        product = a.product if a.product_id is not None else None
        if product is None:
            product = b.product if a.product_id != b.product_id else None
        if product is None:
            obj, created = Product.objects.get_or_create(
                name=sorted((a.name, b.name))[-1],
                quantity='todo',
                certainty=match.score
            )
            assert created
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
