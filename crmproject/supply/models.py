from django.db import models
from suppliers.models import Supplier


class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    delivery_date = models.DateField(auto_now_add=True)
