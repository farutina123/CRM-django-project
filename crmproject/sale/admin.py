from django.contrib import admin
from .models import ProductSale, Sale



class ProductSaleInline(admin.TabularInline):
    model = ProductSale


class SaleAdmin(admin.ModelAdmin):
    inlines = [ProductSaleInline,]
    class Meta:
        model = Sale


admin.site.register(Sale, SaleAdmin)