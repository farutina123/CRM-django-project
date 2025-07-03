from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    confirm_password = serializers.CharField(write_only=True, min_length=4)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']


    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class AttachUserToCompanySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        email = data.get("email")
        if not email:
            raise serializers.ValidationError("Необходимо передать email.")

        try:
            user = User.objects.get(email=email)
            print(user)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден.")

        data['user'] = user
        return data