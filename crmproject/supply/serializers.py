from rest_framework import serializers
from .models import Supply

class SupplyCreateProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        min_value=1,
        help_text="ID товара"
    )
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Количество товара"
    )


class SupplyCreateSerializer(serializers.Serializer):
    storage_id = serializers.IntegerField(
        min_value=1,
    )
    supplier_id = serializers.IntegerField(
        min_value=1,
    )
    products = SupplyCreateProductSerializer(
        many=True,
        help_text='Список товаров в поставке'
    )


class SupplyGetSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    supplier_id = serializers.IntegerField(
        min_value=1,
    )
    delivery_date = serializers.DateField()

    products = SupplyCreateProductSerializer(
        many=True
    )
