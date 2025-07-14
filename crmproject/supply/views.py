from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Supply
from product.models import SupplyProduct
from suppliers.models import Supplier
from storage.models import Storage
from product.models import Product, SupplyProduct
from supply.serializers import SupplyCreateSerializer, SupplyGetSerializer


@extend_schema(
    tags=['supply'],
    request=SupplyCreateSerializer
)
class CreateSupplyView(APIView):
    def post(self, request):
        serializer = SupplyCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if user.company == None:
            return Response('Вы не привязаны к компании', status=status.HTTP_400_BAD_REQUEST)
        supplier_id = serializer.data['supplier_id']
        supplier = get_object_or_404(Supplier, pk=supplier_id)
        if supplier.company != user.company:
            return Response('С данным поставщиком ваша компания не сотрудничает')
        storage = get_object_or_404(Storage, pk=serializer.data['storage_id'])
        if user.company != storage.company:
            return Response('У вас нет склада с таким ID')
        product_list = serializer.data['products']
        for product_item in product_list:
            product = get_object_or_404(Product, pk=product_item['product_id'])
            if product.storage != storage:
                return Response(f'Товар {product_item['product_id']} не привязан к данному складу')
        supply = Supply.objects.create(
            supplier=supplier,
        )
        supply.save()
        for product_item in product_list:
            product = get_object_or_404(Product, pk=product_item['product_id'])
            product.quantity += product_item['quantity']
            product.save()
            supply_product = SupplyProduct.objects.create(
                supply=supply,
                product=product,
                quantity=product_item['quantity']
            )
            supply_product.save()
        supply_id = supply.id
        return Response({"message": "Поставка создана!", "id": supply_id}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['supply'],
    description="Доступно всем сотрудникам компании"
)
class ListGetSupplyView(APIView):
    def get(self, request):
        user = request.user
        supply = Supply.objects.filter(supplier__company=user.company)
        return Response(SupplyGetSerializer(supply, many=True).data, status=status.HTTP_200_OK)


@extend_schema(
    tags=['supply'],
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID'),
    ],
    description="Доступно всем сотрудникам компании"
)
class GetSupplyInvoiceView(APIView):
    def get(self, request, pk=None):
        user = request.user
        supply = get_object_or_404(Supply, pk=pk)
        if user.company != supply.supplier.company:
            return Response('Вы не можете посмотреть данные чужой компании', status=status.HTTP_400_BAD_REQUEST)
        invoice = {}
        product_invoice = {}
        product_list = SupplyProduct.objects.filter(supply_id=pk)
        for item in product_list:
            product_invoice[f'{item.product.title}'] = item.quantity
        invoice['Поставщик'] = supply.supplier.title
        invoice['Товары'] = product_invoice
        invoice['Дата поставки'] = supply.delivery_date
        invoice['Товар принял'] = user.username
        return Response(invoice, status=status.HTTP_200_OK)


