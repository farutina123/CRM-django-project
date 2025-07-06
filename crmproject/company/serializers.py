from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UpdateCompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    INN = serializers.CharField()
    title = serializers.CharField(max_length=200)

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.INN = validated_data.get("INN", instance.INN)
        instance.save()
        return instance


