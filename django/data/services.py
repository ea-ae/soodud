"""Services."""
import itertools as it

from .stores import StoreRegistry, coop, selver
from .models import Store, Product, StoreProduct
from . import text_analysis


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    StoreRegistry.update_stores()


def match(*, size=500_000, start_offset=0):
    """Match products together."""
    # for offset in it.count(start_offset, size):
    #     found = _match_product_set(size, offset)
    #     print(found, offset)
    #     if size != found:
    #         break
    _match_stores(
        StoreProduct.objects.filter(store=1).only('id', 'name').values(),
        StoreProduct.objects.filter(store=2).only('id', 'name').values()
    )


def _match_stores(*args):
    """Find matches between two stores."""
    groups = []
    for store in args:
        # print(store, 'M<<')
        processed_store = text_analysis.prepare_store(store)
        # print(processed_store)
        print('Store processed!')
        groups.append(processed_store)

    matches = text_analysis.find_clusters(groups)
    for match in matches:
        print(match.score,
              StoreProduct.objects.get(id=match.id_a).name,
              StoreProduct.objects.get(id=match.id_b).name)


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
