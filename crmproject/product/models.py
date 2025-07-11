from django.db import models
from storage.models import Storage
from supply.models import Supply


class Product(models.Model):
    title = models.CharField(max_length=200)
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField(default=0)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)


class SupplyProduct(models.Model):
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supplyes')
    quantity = models.IntegerField()
