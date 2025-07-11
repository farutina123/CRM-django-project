from django.contrib import admin
from . import models


@admin.register(models.Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ["id", "supplier", "delivery_date"]

