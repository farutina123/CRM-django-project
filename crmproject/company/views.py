from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CompanySerializer
from drf_spectacular.utils import extend_schema
from .models import Company


@extend_schema(
    tags=['company'],
    request=CompanySerializer
)
class CreateCompanyView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        user = request.user
        print(user)
        print()
        if user.company_id != None:
            return Response('пользователь уже привязан к компании', status=status.HTTP_400_BAD_REQUEST)
        INN = request.data['INN']
        print(user.company_id)
        print(f'мир{request.data}')
        user.save()
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        user.company_id = Company.objects.get(INN=INN)
        user.is_company_owner = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
