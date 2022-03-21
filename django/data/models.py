from django.db import models

from data.stores.products import Discount


class ProductTag(models.Model):
    """Category or tag for a product."""
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Platonic product that all individual store instances point to."""
    name = models.CharField(max_length=250, unique=True)
    image_url = models.TextField(null=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    quantity = models.CharField(max_length=250, default=None, blank=True, null=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    """Store brand."""
    name = models.CharField(unique=True, max_length=250)

    def __str__(self):
        return self.name


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=250)  # store-specific product name
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Price(models.Model):
    """Current or historic price for a store product."""
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)

    # todo: 'current' ought to be in StoreProduct, two-way one-to-one relationship = safer & better
    current = models.BooleanField()  # is the price current, potential optimization over date sort?
    start = models.DateTimeField(auto_now_add=True)  # some stores may specify a manual add/end date
    end = models.DateTimeField(default=None, blank=True, null=True)  # campaign end dates, null for historical prices

    base_price = models.FloatField(default=None, blank=True, null=True)  # null on certain sales or if out of stock
    sale_price = models.FloatField(default=None, blank=True, null=True)  # null if no sale
    members_only = models.BooleanField()

    @property
    def price(self) -> float:
        return self.sale_price if self.sale_price is not None else self.base_price

    @property
    def discount(self) -> Discount:
        if self.members_only and self.sale_price is not None:
            return Discount.MEMBER
        if self.sale_price is None:
            return Discount.NONE
        return Discount.NORMAL

    def __str__(self) -> str:
        return f'{self.price:.2f} @ {self.product.name}'
