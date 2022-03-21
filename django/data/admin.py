from django.contrib import admin
from .models import *


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(StoreProduct)
class StoreProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'last_checked', 'price', 'discount', 'store')
    date_hierarchy = 'last_checked'

    @admin.display()
    def price(self, obj):
        return Price.objects.get(product=obj, current=True).price

    @admin.display()
    def discount(self, obj):
        return Price.objects.get(product=obj, current=True).discount


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'discount', 'base_price', 'sale_price')
    date_hierarchy = 'start'

    @admin.display()
    def product_name(self, obj):
        return obj.product.name
