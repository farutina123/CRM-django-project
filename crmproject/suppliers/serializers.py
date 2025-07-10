from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id",
                  "title",
                  "INN"
                  ]


class SupplierResronseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id",
                  "title",
                  "INN",
                  "company"
                  ]


class UpdateSupplierSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    title = serializers.CharField(max_length=200)
    INN = serializers.CharField(max_length=30)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.INN = validated_data.get('INN', instance.INN)
        instance.save()
        return instance
