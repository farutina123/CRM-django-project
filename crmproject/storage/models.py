from django.db import models
from company.models import Company


class Storage(models.Model):
    address = models.CharField(max_length=200)
    company_id = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='storage')

