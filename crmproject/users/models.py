from django.db import models
from django.contrib.auth.models import Permission, AbstractUser
from company.models import Company
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    confirm_password = models.CharField(max_length=50, default='0000000')
    is_company_owner = models.BooleanField
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

