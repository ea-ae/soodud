"""Serializers."""

from rest_framework import serializers

from data.models import Price, StoreProduct, Product


class TagListField(serializers.SlugRelatedField):
    def to_internal_value(self, data):  # many-to-many field processing
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class PriceSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='discount')

    class Meta:
        model = Price
        fields = ('base_price', 'price', 'type')


class DetailedPriceSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='discount')

    class Meta:
        model = Price
        fields = ('start', 'base_price', 'price', 'type')


class StoreProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name')
    price = PriceSerializer(source='current_price')

    class Meta:
        model = StoreProduct
        fields = ('store_name', 'price')


class DetailedStoreProductSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name')
    prices = DetailedPriceSerializer(source='price_set', many=True)

    class Meta:
        model = StoreProduct
        fields = ('store_name', 'name', 'last_checked', 'prices')


class ProductSerializer(serializers.ModelSerializer):
    store_products = StoreProductSerializer(source='storeproduct_set', many=True)
    price_count = serializers.SerializerMethodField()

    @staticmethod
    def get_price_count(obj: Product):
        return obj.storeproduct_set.count()

    class Meta:
        model = Product
        fields = ('id', 'name', 'store_products', 'price_count')


class DetailedProductSerializer(serializers.ModelSerializer):
    tags = TagListField(slug_field='name', many=True, read_only=True)
    store_products = DetailedStoreProductSerializer(source='storeproduct_set', many=True)

    class Meta:
        model = Product
        fields = ('name', 'quantity', 'tags', 'store_products')
