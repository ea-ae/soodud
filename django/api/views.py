"""Views."""

import os
import pickle
import logging
import itertools as it
from typing import NamedTuple
# from django.contrib.postgres.search import SearchQuery
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from thefuzz import fuzz

from soodud.settings import REST_FRAMEWORK
from data import text_analysis as ta
from . import serializers
from data.models import Product


logger = logging.getLogger('app')


class ProductPagination(pagination.LimitOffsetPagination):
    max_limit = REST_FRAMEWORK['MAX_LIMIT']


CachedProduct = NamedTuple('CachedProduct', id=int, quantities=tuple[ta.Quantity, ...], tokens=set[str])


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    products: list[CachedProduct] = []
    throttle_scope = 'product'
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]

    @classmethod
    def prepare_data(cls):
        """Prepares product data for performant fuzzy searches and stores it in RAM."""
        cls.products = []
        i = 0
        product_count = Product.objects.all().count()
        for product in Product.objects.all().only('id', 'quantity'):  # quantities don't need to be in the db
            i += 1
            if i % 1000 == 0:
                print(f'{i / product_count:.1%}\t {i}/{product_count} products loaded\r', end='')
            text = set(it.chain.from_iterable(
                ta.prepare(x) for x in product.storeproduct_set.values_list('name', flat=True)))
            quantities = tuple(ta.Quantity(q[0], q[1]) for q in product.quantity)
            cls.products.append(CachedProduct(product.id, quantities, text))
        print(f'{i / product_count:.1%}\t {i}/{product_count} products loaded')

    @classmethod
    def load_data(cls):
        if len(cls.products) == 0:
            path = os.path.dirname(__file__) + '/productcache.pickle'
            try:
                cls.products = pickle.load(open(path, 'rb'))
            except OSError:
                cls.create_cache()
            print('Product cache loaded')

    @classmethod
    def create_cache(cls):
        path = os.path.dirname(__file__) + '/productcache.pickle'

        print('Creating product cache...')
        cls.prepare_data()
        pickle.dump(cls.products, open(path, 'wb'))
        print('Product cache created')

    @classmethod
    def match(cls, search_text: str, tokens: set[str],
              quantities: set[ta.Quantity], product: CachedProduct, *, fuzzy=True) -> int:
        """Matches a loaded product with the search query."""
        # quantity score
        q_matches = 0
        for product_qty, search_qty in it.product(product.quantities, quantities):
            if search_qty.unit == product_qty.unit:
                if search_qty.amount != product_qty.amount:
                    return 0
                q_matches += 1
        qty_count = len(product.quantities)
        qty_score = 0 if qty_count == 0 else (q_matches / qty_count) * 100

        # exact score
        matches = len(tokens & product.tokens)
        exact_score = (matches / (0.9 * len(tokens) + 0.1 * len(product.tokens))) * 100  # may go over 100, it's fine

        # fuzzy score
        text_score = exact_score
        if fuzzy and exact_score > 0:  # this will not help in case of short searches full of typos
            pt = ' '.join(sorted(product.tokens))  # as well as this (saves 10% or 100ms/request total!)
            text_score = fuzz.partial_ratio(search_text, pt)

        return int(qty_score * 0.2 + exact_score * 0.5 + text_score * 0.3)

    def get_queryset(self):
        if len(self.products) == 0:  # product cache not loaded
            self.load_data()

        if (search := self.request.query_params.get('search')) and len(search) <= 130:
            logger.info(f'Search query: {search}')

            results: list[tuple[int, int]] = []
            search_tokens = ta.prepare(search)
            search_tokens, search_quantities = ta.parse_quantity(search_tokens, force_extraction=True)
            search_tokens = set(search_tokens)

            if len(search_tokens) == 0:
                return Product.objects.none()

            search_text = ' '.join(sorted(search_tokens))
            for product in self.products:
                score = self.match(search_text, search_tokens, search_quantities, product)
                if score >= 5:
                    results.append((score, product.id))
            results.sort(key=lambda x: -x[0])

            # https://stackoverflow.com/a/25480488/4362799
            ids = [id_ for score, id_ in results[:100]]
            clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(ids)])  # make queryset ordered
            ordering = 'CASE %s END' % clauses
            qs = Product.objects.filter(id__in=ids).extra(
                select={'ordering': ordering}, order_by=('ordering',))
            return qs

        # temporary calls to database for limit/offset API queries
        qs = Product.objects.all()
        if (reverse := self.request.query_params.get('reverse')) and reverse == 'true':
            qs = qs.order_by('-id')[:110]
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailedProductSerializer
        return serializers.ProductSerializer
