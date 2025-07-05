from rest_framework import serializers
from .models import Storage


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = ["id",
            "address"
        ]


class UpdateStorageSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    address = serializers.CharField(max_length=200)

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance