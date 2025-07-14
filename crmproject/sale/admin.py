from django.contrib import admin
from . import models


@admin.register(models.Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["id", "buyer_name", "company", "sale_date"]


@admin.register(models.ProductSale)
class ProductSaleAdmin(admin.ModelAdmin):
    list_display = ["id", "sale", "product", "quantity"]

