from django.urls import path
from .views import CreateSaleView, UpdateSaleView, DeleteSaleView, ListGetSaleView


urlpatterns = [
    path("create/", CreateSaleView.as_view(), name="create-sale"),
    path("update/<int:pk>", UpdateSaleView.as_view(), name="update-sale"),
    path("delete/<int:pk>", DeleteSaleView.as_view(), name="del-sale"),
    path("list", ListGetSaleView.as_view(), name="list-sale")
]