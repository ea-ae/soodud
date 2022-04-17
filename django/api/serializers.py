"""Serializers."""

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from data.models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'quantity']
