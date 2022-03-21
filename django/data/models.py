from django.db import models


class ProductTag(models.Model):
    """Category or tag for a product."""
    name = models.CharField(unique=True, max_length=250)


class Product(models.Model):
    """Platonic product that all individual store instances point to."""
    name = models.CharField(unique=True, max_length=250)
    image_url = models.TextField(null=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    quantity = models.CharField(max_length=250, default=None, blank=True, null=True)


class Store(models.Model):
    """Store brand."""
    name = models.CharField(unique=True, max_length=250)


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=250)  # store-specific product name
    last_checked = models.DateTimeField(auto_now=True)


class Price(models.Model):
    """Current or historic price for a store product."""
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)

    current = models.BooleanField()  # is the price current, potential optimization over date sort?
    start = models.DateTimeField(auto_now_add=True)  # some stores may specify a manual add/end date
    end = models.DateTimeField(default=None, blank=True, null=True)  # campaign end dates, null for historical prices

    base_price = models.IntegerField(default=None, blank=True, null=True)  # null on certain sales or if out of stock
    sale_price = models.IntegerField(default=None, blank=True, null=True)  # null if no sale
    members_only = models.BooleanField()
