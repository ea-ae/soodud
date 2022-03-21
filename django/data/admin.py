from django.contrib import admin
from .models import *


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)

    # @admin.display()
    # def tags_(self, obj: ProductTag):
    #     tags = obj.tags.through.objects.all().count()
    #     return tags


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'products')

    @admin.display()
    def products(self, obj):
        return f'{StoreProduct.objects.filter(store=obj).count()} products'


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
