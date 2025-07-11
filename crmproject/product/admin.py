from django.contrib import admin
from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "purchase_price", "sale_price", "quantity", "storage"]


@admin.register(models.SupplyProduct)
class SupplyProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "supply", "quantity"]