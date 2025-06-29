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
        print(user.is_company_owner)
        if user.company_id != None:
            return Response('пользователь уже привязан к компании', status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        company = serializer.save()
        user.company_id = company
        user.is_company_owner = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
