from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean_password2(self, validated_data):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords don't match")
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        user.save()

        return user

    # def create(self, validated_data):
    #     user = User.objects.create_user(
    #         username=validated_data['username'],
    #         password=validated_data['password'],
    #     )
    #     user.save()
    #
    #     return user