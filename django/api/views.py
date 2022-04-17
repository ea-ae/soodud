"""Views."""

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import pagination

from . import serializers
from data.models import Product


class ProductPagination(pagination.LimitOffsetPagination):
    max_limit = 100


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailedProductSerializer
        return serializers.ProductSerializer
