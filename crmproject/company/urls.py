from django.urls import path
from .views import CreateCompanyView, DeleteCompanyView


urlpatterns = [
    path("create/", CreateCompanyView.as_view(), name="create-company"),
    path("delete/", DeleteCompanyView.as_view(), name="delete-company"),
    path("delete/<int:{id}>/", DeleteCompanyView.as_view())]

