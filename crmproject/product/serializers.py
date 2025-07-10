from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
            "title",
            "purchase_price",
            "sale_price"
        ]


class ResponseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id",
            "title",
            "purchase_price",
            "sale_price",
            "quantity",
            "storage"
        ]


class UpdateProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    title = serializers.CharField(max_length=200)
    purchase_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=6, decimal_places=2)


    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.purchase_price = validated_data.get('purchase_price', instance.purchase_price)
        instance.sale_price = validated_data.get('sale_price', instance.sale_price)
        instance.save()
        return instance