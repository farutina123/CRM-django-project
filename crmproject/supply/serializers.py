from rest_framework import serializers


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
