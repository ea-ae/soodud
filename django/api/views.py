"""Views."""

from django.contrib.postgres.search import SearchQuery
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.authentication import SessionAuthentication
import pickle
import os
from timeit import default_timer as timer
import itertools as it
from typing import NamedTuple
from thefuzz import fuzz

from soodud.settings import REST_FRAMEWORK
from data import text_analysis as ta
from . import serializers
from data.models import Product


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ProductPagination(pagination.LimitOffsetPagination):
    max_limit = REST_FRAMEWORK['MAX_LIMIT']


CachedProduct = NamedTuple('CachedProduct', id=int, quantities=tuple[ta.Quantity, ...], text=str)


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
        for product in Product.objects.all().only('id', 'quantity'):  # quantities don't need to be in the db
            i += 1
            if i % 1000 == 0:
                print(i)
            text = ' '.join(' '.join(ta.prepare(x)) for x in product.storeproduct_set.values_list('name', flat=True))
            quantities = tuple(ta.Quantity(q[0], q[1]) for q in product.quantity)
            cls.products.append(CachedProduct(product.id, quantities, text))

    @classmethod
    def load_data(cls):
        if len(cls.products) == 0:
            path = os.path.dirname(__file__) + '/productcache.pickle'
            try:
                cls.products = pickle.load(open(path, 'rb'))
            except OSError:
                print('Creating product cache...')
                cls.prepare_data()
                pickle.dump(cls.products, open(path, 'wb'))
                print('Product cache created')
            else:
                print('Product cache loaded')

    @classmethod
    def match(cls, tokens: list[str], quantities: set[ta.Quantity], product: CachedProduct, *, fuzzy=False) -> int:
        """Matches a loaded product with the search query."""
        # quantity score
        qty_score = 0
        q_matches = 0
        for product_qty, search_qty in it.product(product.quantities, quantities):
            if search_qty.unit == product_qty.unit:
                if search_qty.amount != product_qty.amount:
                    return 0
                q_matches += 1
        qty_count = len(product.quantities)
        qty_score = 0 if qty_count == 0 else (q_matches / qty_count) * 100

        # exact score
        exact_score = 0
        product_tokens = product.text.split()
        matches = sum(product_token in tokens for product_token in product_tokens)
        exact_score = (matches / max(len(tokens), len(product_tokens))) * 100

        # fuzzy score
        text_score = 100
        if fuzzy:
            # text_score = fuzz.partial_ratio(' '.join(tokens), product.text)
            text_score = fuzz.partial_token_sort_ratio(' '.join(tokens), product.text, force_ascii=False)

        return int(qty_score * 0.2 + exact_score * 0.5 + text_score * 0.3)

    def get_queryset(self):
        start = timer()
        self.load_data()

        if (search := self.request.query_params.get('search')) and len(search) <= 130:
            results: list[tuple[int, int]] = []
            search_tokens = ta.prepare(search)
            search_tokens, search_quantities = ta.parse_quantity(search_tokens)
            start2 = timer()
            for product in self.products:
                score = self.match(list(search_tokens), search_quantities, product)
                # if score >= 10:
                results.append((score, product.id))
            print(f'Data search took {(timer() - start2) * 1000}ms with "{search}"')
            results.sort(key=lambda x: -x[0])

            # https://stackoverflow.com/a/25480488/4362799
            ids = [id_ for score, id_ in results[:100]]
            clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(ids)])
            ordering = 'CASE %s END' % clauses
            qs = Product.objects.filter(id__in=ids).extra(
                select={'ordering': ordering}, order_by=('ordering',))

            # print(results[:100])
            # x = list(qs)
            print(f'New search query took {(timer() - start) * 1000}ms with "{search}"')
            return qs

        qs = Product.objects.all()

        if (search := self.request.query_params.get('oldsearch')) and len(search) <= 130:
            # start = timer()
            # qs = qs.filter(storeproduct__name__search=search)  # ~170-250ms
            qs = qs.filter(name__search=search)  # about the same??
            # x = list(qs[:100])
            # print(f'Search query took {(timer() - start) * 1000}ms with "{search}"')

        if (reverse := self.request.query_params.get('reverse')) and reverse == 'true':
            qs = qs.order_by('-id')

        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailedProductSerializer
        return serializers.ProductSerializer
