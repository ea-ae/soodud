from django.db import models


class ProductTag(models.Model):
    """Category or tag for a product."""
    name = models.CharField(max_length=250)


class Product(models.Model):
    """Platonic product that all individual store instances point to."""
    name = models.CharField(max_length=250)
    image_url = models.TextField(null=True)
    tags = models.ManyToManyField(ProductTag, blank=True, null=True)


class Store(models.Model):
    """Store."""
    name = models.CharField(max_length=250)


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=250)  # store-specific product name
    last_checked = models.DateTimeField(auto_now=True)


class Price(models.Model):
    """Current or historic price for a store product."""
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)

    current = models.BooleanField()  # is the price current, potential optimization over date sort?
    start = models.DateTimeField(auto_now_add=False)  # some stores may specify a manual add/end date
    end = models.DateTimeField(blank=True, null=True)  # store-provided campaign end dates, null for historical prices

    base_price = models.IntegerField(blank=True, null=True)  # null if out of stock / unavailable
    sale_price = models.IntegerField(blank=True, null=True)  # null if no sale
    members_only = models.BooleanField()
