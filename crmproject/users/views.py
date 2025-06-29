from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer
from .models import User
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=['user']
)
class UserRegistrationView(CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer
# Create your views here.
