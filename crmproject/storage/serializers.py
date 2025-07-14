from rest_framework import serializers
from .models import Storage



class StorageProductSerializer(serializers.Serializer):
    title = serializers.CharField(
        min_length=3
    )
    quantity = serializers.IntegerField(
        min_value=1,
        help_text="Количество товара"
    )


class StorageSerializer(serializers.ModelSerializer):
    product = StorageProductSerializer(many=True)
    class Meta:
        model = Storage
        fields = ["id",
            "address",
            "product"
        ]


class UpdateStorageSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    address = serializers.CharField(max_length=200)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance