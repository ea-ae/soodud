"""Views."""

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import ProductSerializer
from data.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
