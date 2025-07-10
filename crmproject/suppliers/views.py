from django.shortcuts import get_object_or_404
from django.views import generic
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Supplier
from django.db import IntegrityError
from .serializers import SupplierSerializer, SupplierResronseSerializer, UpdateSupplierSerializer


@extend_schema(
    tags=['supplier'],
    request=SupplierSerializer
)
class CreateSupplierView(APIView):
    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.company == None:
            return Response('Вы не привязаны к компании', status=status.HTTP_400_BAD_REQUEST)
        supplier = Supplier.objects.create(
            title=serializer.data['title'],
            INN=serializer.data['INN'],
            company=user.company,
        )
        supplier.save()
        response_serializer = SupplierResronseSerializer(instance=supplier)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['supplier']
)
class ListSupplierView(APIView):
    def get(self, request):
        user = request.user
        supplier = Supplier.objects.filter(company=user.company)
        return Response(SupplierSerializer(supplier, many=True).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['supplier'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Доступно всем сотрудникам компании"
)
class GetSupplierView(APIView):
    def get(self, request, pk=None):
        user = request.user
        supplier = get_object_or_404(Supplier, pk=pk)
        if user.company != supplier.company:
            return Response('Вы не можете посмотреть данные чужой компании', status=status.HTTP_400_BAD_REQUEST)
        return Response(SupplierSerializer(supplier).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['supplier'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    request=UpdateSupplierSerializer,
    description="Обновление информации о поставщике доступно всем авторизованным пользователям, привязанным к компании"
)
class UpdateSupplierView(APIView):
    def put(self, request, pk=None):
        user = request.user
        supplier = get_object_or_404(Supplier, pk=pk)
        if user.company != supplier.company:
            return Response('Данные о поставщиках других компаний недоступны', status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateSupplierSerializer(data=request.data, instance=supplier)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['supplier'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Удаление информации о поставщике доступно всем авторизованным пользователям, привязанным к компании"
)
class DeleteSupplierView(APIView):
    def delete(self, request, pk=None):
        supplier = get_object_or_404(Supplier, pk=pk)
        user = request.user
        if user.company != supplier.company:
            return Response('Нельзя удалить поставщика другой компании', status=status.HTTP_400_BAD_REQUEST)
        title = supplier.title
        supplier.delete()
        return Response(f"Поставщик '{title}' успешно удален", status=status.HTTP_200_OK)