from django.db import models
from company.models import Company
from product.models import Product


class Sale(models.Model):
    buyer_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)


class ProductSale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='product_sales')
    quantity = models.IntegerField()
