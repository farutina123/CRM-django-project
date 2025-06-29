from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("register/", views.UserRegistrationView.as_view(), name="register")]


# from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
# from . import views
# from rest_framework.routers import DefaultRouter
# from django.urls import include, path
# from . import views
#
# router = DefaultRouter()
# router.register("register/", views.UserRegistrationView.as_view(), basename='register')
#
# urlpatterns = [
#     path("", include(router.urls)),
# ]