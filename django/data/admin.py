"""Admin pages."""

from django.contrib import admin
from .models import *


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('price_list',)
    list_display = ('id', 'name', 'cheapest_store_name', 'cheapest_store_price', 'tags_')
    search_fields = ('name',)

    @admin.display()
    def price_list(self, obj):
        prices = sorted(self.get_prices(obj), key=lambda p: p.price)
        return '\n'.join(f'{price.price} @ {price.product.store.name}' for price in prices)

    @staticmethod
    def get_prices(obj: Product):
        products = StoreProduct.objects.filter(product=obj).only('current_price')
        return [product.current_price for product in products]

    @admin.display()
    def cheapest_store_name(self, obj):
        prices = self.get_prices(obj)
        store = None if len(prices) == 0 else min(prices, key=lambda x: x.price)
        return store.product.store.name if store is not None else None

    @admin.display()
    def cheapest_store_price(self, obj: Product):
        prices = self.get_prices(obj)
        store = None if len(prices) == 0 else min(prices, key=lambda x: x.price)
        return store.price if store is not None else None

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
    readonly_fields = ('price_history',)

    list_display = ('id', 'name', 'last_checked', 'price', 'store', 'hash', 'has_barcode')
    search_fields = ('name', 'store__name', 'hash')
    date_hierarchy = 'last_checked'

    @admin.display()
    def price(self, obj):
        return obj.current_price.price

    @admin.display()
    def price_history(self, obj):
        return '\n'.join(str(f'{price.price} @ {str(price.start)}')
                         for price
                         in Price.objects.filter(product=obj).defer('product', 'members_only')[:10])

    @admin.display()
    def discount(self, obj):
        return obj.current_price.discount


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    raw_id_fields = ('product',)
    readonly_fields = ('id', 'start', 'discount')

    list_display = ('id', 'product_name', 'price', 'discount', 'start', 'base_price', 'sale_price')
    search_fields = ('product__name',)
    date_hierarchy = 'start'

    @admin.display()
    def product_name(self, obj):
        return obj.product.name
