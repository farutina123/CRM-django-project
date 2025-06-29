from django.urls import path
from .views import CreateCompanyView


urlpatterns = [
    path("create-company/", CreateCompanyView.as_view(), name="create-product")]

