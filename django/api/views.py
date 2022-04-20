"""Views."""

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from . import serializers
from data.models import Product


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ProductPagination(pagination.LimitOffsetPagination):
    max_limit = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    throttle_scope = 'product'
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailedProductSerializer
        return serializers.ProductSerializer
