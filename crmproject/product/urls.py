from django.urls import path
from .views import CreateProductView, UpdateProductView, DeleteProductView, GetProductView, ListGetProductView

urlpatterns = [
    path("create/", CreateProductView.as_view(), name="create-product"),
    path("update/<int:pk>/", UpdateProductView.as_view(), name="update-product"),
    path("delete/<int:pk>/", DeleteProductView.as_view(), name="delete-product"),
    path("<int:pk>/", GetProductView.as_view(), name="get-product"),
    path("list/", ListGetProductView.as_view(), name="list-product")]
