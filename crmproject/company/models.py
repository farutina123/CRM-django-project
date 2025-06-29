from django.db import models

class Company(models.Model):
    INN = models.CharField(unique=True)
    title = models.CharField(max_length=200)
