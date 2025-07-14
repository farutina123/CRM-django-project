from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import SaleProductSerializer, UpdateSaleSerializer, SaleGetSerializer
from .models import Sale, ProductSale
from suppliers.models import Supplier
from storage.models import Storage
from product.models import Product, SupplyProduct
from supply.serializers import SupplyCreateSerializer, SupplyGetSerializer
from supply.models import Supply
from datetime import date, datetime


@extend_schema(
    tags=['sale'],
    request=SaleProductSerializer
)
class CreateSaleView(APIView):
    def post(self, request):
        serializer = SaleProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.company == None:
            return Response('Вы не привязаны к компании', status=status.HTTP_400_BAD_REQUEST)
        product_list = serializer.data['product_sales']
        error_dict = {}
        for product_item in product_list:
            product = get_object_or_404(Product, pk=product_item['product_id'])
            if product.storage != user.company.storage:
                return Response(f'Товар {product_item['product_id']} не привязан к складу вашей компании')
            if product.quantity < product_item['quantity']:
                error_dict[f'{product.title} в наличии только'] = product.quantity
        if error_dict != {}:
            return Response(error_dict, status=status.HTTP_400_BAD_REQUEST)
        sale = Sale.objects.create(
            buyer_name=serializer.data['buyer_name'],
            company=user.company
        )
        sale.save()
        for product_item in product_list:
            product = get_object_or_404(Product, pk=product_item['product_id'])
            product.quantity -= product_item['quantity']
            product.save()
            sale_product = ProductSale.objects.create(
                product=product,
                sale=sale,
                quantity=product_item['quantity']
            )
            sale_product.save()
        sale_id = sale.id
        return Response({"message": "Продажа состоялась!", "id": sale_id}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['sale'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    request=UpdateSaleSerializer,
    description="Доступно всем сотрудникам компании"
)
class UpdateSaleView(APIView):
    def put(self, request, pk=None):
        user = request.user
        sale = get_object_or_404(Sale, pk=pk)
        if user.company != sale.company:
            return Response('Вы не привязаны к данной компании', status=status.HTTP_400_BAD_REQUEST)
        serializer = UpdateSaleSerializer(data=request.data, instance=sale)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['sale'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Доступно всем пользователям компании"
)
class DeleteSaleView(APIView):
    def delete(self, request, pk=None):
        sale = get_object_or_404(Sale, pk=pk)
        sale_buyer = sale.buyer_name
        sale_date = sale.sale_date
        user = request.user
        if user.company != sale.company:
            return Response('Вы не можете удалить продажу другой компании', status=status.HTTP_400_BAD_REQUEST)
        product_sale_list = ProductSale.objects.filter(sale=sale)
        for item in product_sale_list:
            product_id = item.product.id
            print(f"id {product_id} : item_quantity({item.quantity})")
            product = get_object_or_404(Product, pk=product_id)
            product.quantity += item.quantity
            product.save()
        sale.delete()
        return Response(f"Продажа '{pk}' покупателю {sale_buyer} от {sale_date} успешно удалена", status=status.HTTP_200_OK)


@extend_schema(
    tags=['sale'],
    description="Доступно всем сотрудникам компании"
)
class ListGetSaleView(APIView):
    def get(self, request):
        user = request.user
        sale = Sale.objects.filter(company=user.company)
        return Response(SaleGetSerializer(sale, many=True).data, status=status.HTTP_200_OK)
