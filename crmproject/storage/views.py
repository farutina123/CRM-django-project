from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StorageSerializer, UpdateStorageSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Storage
from django.db import IntegrityError


@extend_schema(
    tags=['storage'],
    description="Cоздание склада доступно только владельцу компании",
    request=StorageSerializer
)
class CreateStorageView(APIView):
    def post(self, request):
        serializer = StorageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if not user.is_company_owner:
            return Response('Вы не владелец компании', status=status.HTTP_400_BAD_REQUEST)
        if user.company == None:
            return Response('Вы не привязаны к компании', status=status.HTTP_400_BAD_REQUEST)
        try:
            storage = Storage.objects.create(
                address=serializer.data['address'],
                company=user.company,
            )
        except IntegrityError:
            return Response('У данной компании уже есть склад', status=500)
        storage.save()
        response_serializer = StorageSerializer(instance=storage)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['storage'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    request=UpdateStorageSerializer,
    description="Обновление информации о складе доступно только владельцу компании"
)
class UpdateStorageView(APIView):
    def put(self, request, pk=None):
        user = request.user
        storage = get_object_or_404(Storage, pk=pk)
        if not user.is_company_owner:
            return Response('Вы не владелец компании', status=status.HTTP_400_BAD_REQUEST)
        if user.company == None:
            return Response('Вы не привязаны к компании', status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateStorageSerializer(data=request.data, instance=storage)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['storage'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Удвление информации о складе доступно только владельцу компании"
)
class DeleteStorageView(APIView):
    def delete(self, request, pk=None):
        storage = get_object_or_404(Storage, pk=pk)
        user = request.user
        if not user.is_company_owner:
            return Response('Только владелец может удалить склад', status=status.HTTP_400_BAD_REQUEST)
        if user.company != storage.company:
            return Response('Вы не можете удалить чужой склад', status=status.HTTP_400_BAD_REQUEST)
        address = storage.address
        storage.delete()
        return Response(f"Склад по данному адресу '{address}' успешно удален", status=status.HTTP_200_OK)


@extend_schema(
    tags=['storage'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Просматривать информацию о складе может любой работник, прикрепленный к компании"
)
class GetStorageView(APIView):
    def get(self, request, pk=None):
        user = request.user
        storage = get_object_or_404(Storage, pk=pk)
        if user.company != storage.company:
            return Response('Вы не можете посмотреть данные чужой компании', status=status.HTTP_400_BAD_REQUEST)
        return Response(StorageSerializer(storage).data, status=status.HTTP_200_OK)