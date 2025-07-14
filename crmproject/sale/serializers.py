from rest_framework import serializers
from .models import Sale, ProductSale
from supply.serializers import SupplyCreateProductSerializer
from datetime import date, datetime
from rest_framework import status
from rest_framework.response import Response


class SaleProductSerializer(serializers.Serializer):
    buyer_name = serializers.CharField(
        min_length=4
    )
    product_sales = SupplyCreateProductSerializer(
        many=True,
        help_text='Список товаров в поставке'
    )


class UpdateSaleSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    buyer_name = serializers.CharField(
        min_length=4
    )
    sale_date = serializers.DateField()


    def validate(self, data):
        if (data.get('sale_date') > date.today()):
            raise serializers.ValidationError('новая дата не должна превышать текущую')
        return data

    def update(self, instance, validated_data):
        instance.buyer_name = validated_data.get('buyer_name', instance.buyer_name)
        instance.sale_date = validated_data.get('sale_date', instance.sale_date)
        instance.save()
        return instance


class SaleGetSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    buyer_name = serializers.CharField(
        min_length=4
    )
    sale_date = serializers.DateField()