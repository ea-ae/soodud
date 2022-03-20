from django.db import models


class Product(models.Model):
    """Platonic product that all individual store instances point to."""
    name = models.CharField(max_length=250)
    description = models.TextField(null=True)
    image_url = models.TextField(null=True)


class Store(models.Model):
    """Store."""
    name = models.CharField(max_length=50)


class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    name = models.CharField(max_length=250)  # store-specific product name
    last_checked = models.DateTimeField(auto_now=True)


class Price(models.Model):
    """Current or historic price for a store product."""
    product = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)

    current = models.BooleanField()  # is the price current, potential optimization over date sort?
    start = models.DateTimeField(auto_now_add=False)  # some stores may specify a manual add-end date
    end = models.DateTimeField(null=True)  # store-provided campaign end dates, null for historical prices

    base_price = models.IntegerField()
    sale_price = models.IntegerField(null=True)  # null if no sale
    members_only = models.BooleanField()
