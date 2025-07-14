from django.db import models
from suppliers.models import Supplier


class Supply(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='supply')
    delivery_date = models.DateField(auto_now_add=True)
