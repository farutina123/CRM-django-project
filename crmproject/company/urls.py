from django.urls import path
from .views import CreateCompanyView, DeleteCompanyView, UpdateCompanyView, GetCompanyView


urlpatterns = [
    path("create/", CreateCompanyView.as_view(), name="create-company"),
    path("delete/<int:pk>/", DeleteCompanyView.as_view()),
    path("update/<int:pk>/", UpdateCompanyView.as_view()),
    path("<int:pk>/", GetCompanyView.as_view())]

