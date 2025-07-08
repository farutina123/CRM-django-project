from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Supplier
from django.db import IntegrityError
from .serializers import SupplierSerializer, SupplierResronseSerializer


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