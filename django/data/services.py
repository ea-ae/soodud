"""Services."""
import itertools as it

from .stores import StoreRegistry


def launch():
    """Update stores, for use by task schedulers and interactive shells."""
    from .stores import coop, selver, rimi
    StoreRegistry.update_stores()


def match(*, size=500_000, start_offset=0):
    """Match products together."""
    # stores = [StoreProduct.objects.filter(store=store.id).values('id', 'name')
    #           for store in Store.objects.only('id').all()]
    from .stores import selver
    StoreRegistry.match_stores()


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
