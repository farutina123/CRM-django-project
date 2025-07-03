from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, AttachUserToCompanySerializer
from .models import User
from drf_spectacular.utils import extend_schema
@extend_schema(
    tags=['user']
)
class UserRegistrationView(CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer


@extend_schema(
    tags=['user'],
    description="Добавлять сотрудника может только владелец компании",
    request=AttachUserToCompanySerializer
)
class AttachUserToCompanyView(APIView):

    def post(self, request):
        serializer = AttachUserToCompanySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        add_user = serializer.validated_data['user']
        user = request.user
        if not user.is_company_owner:
            return Response(f"Вы не владелец компании", status=400)
        if add_user == user:
            return Response(f"Вы уже владелец компании", status=400)
        if add_user.company != None:
            return Response("пользователь уже привязан к компании", status=400)
        add_user.company = user.company
        add_user.save()
        return Response(f"пользователь {add_user.username} добавлен в компанию", status=200)
