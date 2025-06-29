from django.db import models
from django.contrib.auth.models import Permission, AbstractUser
from company.models import Company
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_company_owner = models.BooleanField(default=False)
    company_id = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

