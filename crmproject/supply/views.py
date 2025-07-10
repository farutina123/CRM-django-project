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
from .serializers import SupplyCreateSerializer


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
        supply = Supply.objects.create(
            supplier=serializer.data['supplier_id'],
        )
        supply_product = SupplyProduct.objects.create(

        )
        supply.save()
        response_serializer = SupplierResronseSerializer(instance=supplier)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
