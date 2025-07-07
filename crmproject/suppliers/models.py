from django.db import models
from company.models import Company


class Supplier(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    INN = models.CharField(unique=True)