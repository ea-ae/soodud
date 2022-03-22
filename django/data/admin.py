"""Admin pages."""

from django.contrib import admin
from .models import *


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cheapest_store_name', 'cheapest_store_price', 'tags_')
    search_fields = ('name',)

    @staticmethod
    def cheapest_store(obj: Product):
        products = StoreProduct.objects.filter(product=obj)
        prices = []
        for product in products[::-1]:
            prices.append(product.current_price)
        return min(prices, key=lambda x: x.price)

    @admin.display()
    def cheapest_store_name(self, obj):
        return self.cheapest_store(obj).product.store.name

    @admin.display()
    def cheapest_store_price(self, obj: Product):
        return self.cheapest_store(obj).price

    @admin.display()
    def tags_(self, obj: Product):
        return ', '.join(tag.producttag.name for tag in obj.tags.through.objects.filter(product=obj))


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'products')

    @admin.display()
    def products(self, obj):
        return StoreProduct.objects.filter(store=obj).count()


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('current_price',)  # 'product'

    list_display = ('id', 'name', 'last_checked', 'price', 'store')
    search_fields = ('name', 'store__name')
    date_hierarchy = 'last_checked'

    @admin.display()
    def price(self, obj):
        return obj.current_price.price

    @admin.display()
    def discount(self, obj):
        return obj.current_price.discount


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)
    readonly_fields = ('id', 'start', 'discount')

    list_display = ('id', 'product_name', 'price', 'discount', 'base_price', 'sale_price')
    search_fields = ('product_name', 'discount')
    date_hierarchy = 'start'

    @admin.display()
    def product_name(self, obj):
        return obj.product.name
