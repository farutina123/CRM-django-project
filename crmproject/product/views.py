from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProductSerializer, UpdateProductSerializer, ResponseProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiRequest
from .models import Product
from storage.models import Storage
from django.db import IntegrityError


@extend_schema(
    tags=['product'],
    description="Доступно всем сотрудникам компании",
    request=OpenApiRequest(
        request={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string"
                },
                "purchase_price": {
                    "type": "string",
                    "example": "1500.00"
                },
                "sale_price": {
                    "type": "string",
                    "example": "3120.99"
                }
            }
        }
    )
)
class CreateProductView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.company == None:
            return Response('Вы не привязаны к компании', status=status.HTTP_400_BAD_REQUEST)

        if (float(serializer.data['purchase_price']) < 0) or (float(serializer.data['sale_price']) < 0):
            return Response('цена должна быть положительной', status=status.HTTP_400_BAD_REQUEST)
        storage = Storage.objects.filter(company=user.company).first()
        product = Product.objects.create(
            title=serializer.data['title'],
            purchase_price=serializer.data['purchase_price'],
            sale_price=serializer.data['sale_price'],
            storage=storage
        )
        product.save()
        response_serializer = ResponseProductSerializer(instance=product)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['product'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    request=OpenApiRequest(
        request={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string"
                },
                "purchase_price": {
                    "type": "string",
                    "example": "1500.00"
                },
                "sale_price": {
                    "type": "string",
                    "example": "3120.99"
                }
            }
        }
    ),
    description="Доступно всем сотрудникам компании"
)
class UpdateProductView(APIView):
    def put(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        if user.company != product.storage.company:
            return Response('Вы не привязаны к данной компании', status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateProductSerializer(data=request.data, instance=product)
        serializer.is_valid(raise_exception=True)
        if (float(serializer.data['purchase_price']) < 0) or (float(serializer.data['sale_price']) < 0):
            return Response('цена должна быть положительной', status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['product'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Доступно всем пользователям компании"
)
class DeleteProductView(APIView):
    def delete(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        user = request.user
        if user.company != product.storage.company:
            return Response('Вы не можете удалить продукты другой компании', status=status.HTTP_400_BAD_REQUEST)
        title = product.title
        product.delete()
        return Response(f"Продукт '{title}' успешно удален", status=status.HTTP_200_OK)


@extend_schema(
    tags=['product'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Доступно всем сотрудникам компании"
)
class GetProductView(APIView):
    def get(self, request, pk=None):
        user = request.user
        product = get_object_or_404(Product, pk=pk)
        if user.company != product.storage.company:
            return Response('Вы не можете посмотреть данные чужой компании', status=status.HTTP_400_BAD_REQUEST)
        return Response(ResponseProductSerializer(product).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['product'],
    description="Доступно всем сотрудникам компании"
)
class ListGetProductView(APIView):
    def get(self, request):
        user = request.user
        products = Product.objects.filter(storage__company=user.company)
        return Response(ProductSerializer(products, many=True).data, status=status.HTTP_200_OK)

