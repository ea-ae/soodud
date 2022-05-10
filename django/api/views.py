"""Views."""

from typing import NamedTuple
import itertools as it
import logging
import os
import pickle

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import pagination
from rest_framework import permissions
from rest_framework import viewsets
from thefuzz import fuzz

from . import serializers
from data import text_analysis as ta
from data.models import Product, StoreProduct
from soodud.settings import REST_FRAMEWORK


logger = logging.getLogger('app')


CachedProduct = NamedTuple('CachedProduct', id=int, quantities=tuple[ta.Quantity, ...], tokens=set[str], sp_count=int)


class ProductPagination(pagination.LimitOffsetPagination):
    max_limit = REST_FRAMEWORK['MAX_LIMIT']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    products: list[CachedProduct] = []
    throttle_scope = 'product'
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]

    @method_decorator(cache_page(3600))
    def dispatch(self, *args, **kwargs):
        """Cache all API calls."""
        return super().dispatch(*args, **kwargs)

    @classmethod
    def prepare_data(cls):
        """Prepare product data for faster search queries and store it in RAM."""
        progress_i = 0
        cls.products = []
        product_count = Product.objects.all().count()
        for product in Product.objects.all().only('id', 'quantity'):
            progress_i += 1
            if progress_i % 1000 == 0:
                print(f'{progress_i / product_count:.1%}\t {progress_i}/{product_count} products loaded\r', end='')

            text = set(it.chain.from_iterable(  # concat all store product names
                ta.prepare(x) for x in product.storeproduct_set.values_list('name', flat=True)))
            quantities = tuple(ta.Quantity(q[0], q[1]) for q in product.quantity)
            sp_count = StoreProduct.objects.filter(product=product).count()
            cls.products.append(CachedProduct(product.id, quantities, text, sp_count))
        print(f'{progress_i / product_count:.1%}\t {progress_i}/{product_count} products loaded')

    @classmethod
    def load_data(cls):
        """Load pickled product data into memory."""
        if len(cls.products) == 0:
            path = os.path.dirname(__file__) + '/productcache.pickle'
            try:
                cls.products = pickle.load(open(path, 'rb'))
            except OSError:
                cls.create_cache()
            print('Product cache loaded')

    @classmethod
    def create_cache(cls):
        """Pickle product data for later cache loads."""
        path = os.path.dirname(__file__) + '/productcache.pickle'

        print('Creating product cache...')
        cls.prepare_data()
        pickle.dump(cls.products, open(path, 'wb'))
        print('Product cache created')

    @classmethod
    def match(cls, search_text: str, tokens: set[str],
              quantities: set[ta.Quantity], product: CachedProduct, *, fuzzy=True) -> int:
        """Matches a loaded product with the search query."""
        q_matches = 0  # quantity score
        for product_qty, search_qty in it.product(product.quantities, quantities):
            if search_qty.unit == product_qty.unit:
                if search_qty.amount != product_qty.amount:
                    return 0
                q_matches += 1
        qty_count = len(product.quantities)
        qty_score = 0 if qty_count == 0 else (q_matches / qty_count) * 100

        token_matches = len(tokens & product.tokens)  # exact score
        exact_score = (token_matches / (0.9 * len(tokens) + 0.1 * len(product.tokens))) * 100

        price_score = product.sp_count / 0.04  # price count score (more stores have product = more relevance)

        text_score = exact_score  # fuzzy score
        if fuzzy and 100 > exact_score > 0:  # this will not help in case of short searches full of typos
            pt = ' '.join(sorted(product.tokens))  # as well as this (saves 10% or 100ms/request total!)
            text_score = fuzz.partial_ratio(search_text, pt)

        return int(qty_score * 0.2 + exact_score * 0.5 + price_score * 0.2 + text_score * 0.2)

    def get_queryset(self):
        """Get API call queryset with a custom override for search queries."""
        if len(self.products) == 0:  # product cache not loaded
            self.load_data()

        search = self.request.query_params.get('search')
        # search = '' if search is None else search
        if search and len(search) <= 130:
            logger.info(f'Search query: {search}')

            results: list[tuple[int, int]] = []
            search_tokens = ta.prepare(search)
            search_tokens, search_quantities = ta.parse_quantity(search_tokens, force_extraction=True)
            search_tokens = set(search_tokens)

            # if len(search_tokens) == 0:
            #     return Product.objects.none()

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

        # temporary(?) calls to database for limit/offset API queries
        qs = Product.objects.all()
        if (reverse := self.request.query_params.get('reverse')) and reverse == 'true':
            qs = qs.order_by('-id')[:110]
        return qs

    def get_serializer_class(self):
        """Get appropriate serializer class depending on API call type."""
        if self.action == 'retrieve':
            return serializers.DetailedProductSerializer
        return serializers.ProductSerializer
