from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import StorageSerializer
from drf_spectacular.utils import extend_schema
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)
