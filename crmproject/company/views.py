from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CompanySerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes


@extend_schema(
    tags=['company'],
    description="Создание компании доступно только авторизованным пользователям",
    request=CompanySerializer
)
class CreateCompanyView(APIView):
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        user = request.user
        if user.company != None:
            return Response('пользователь уже привязан к компании', status=status.HTTP_400_BAD_REQUEST)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        company = serializer.save()
        user.company = company
        user.is_company_owner = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['company'],
    description="Удаление компании доступно только авторизованным пользователям",
    parameters=[
        OpenApiParameter(name='id', type=OpenApiTypes.INT, location=OpenApiParameter.PATH, description='ID')
    ]
)
class DeleteCompanyView(APIView):
    permission_classes = []
    def delete(self, request, pk=None):
        print(pk)
