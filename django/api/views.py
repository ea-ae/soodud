"""Views."""

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from timeit import default_timer as timer

from soodud.settings import REST_FRAMEWORK
from . import serializers
from data.models import Product


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ProductPagination(pagination.LimitOffsetPagination):
    max_limit = REST_FRAMEWORK['MAX_LIMIT']


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    # queryset = Product.objects.all()
    throttle_scope = 'product'
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['id']

    def get_queryset(self):
        qs = Product.objects.all()
        if (search := self.request.query_params.get('search')) and len(search) <= 130:
            qs = qs.filter(storeproduct__name__search=search)
        if (reverse := self.request.query_params.get('reverse')) and reverse == 'true':
            qs = qs.order_by('-id')
        return qs

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailedProductSerializer
        return serializers.ProductSerializer
