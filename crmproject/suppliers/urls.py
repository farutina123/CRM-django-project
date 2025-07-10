from django.urls import path
from .views import CreateSupplierView, ListSupplierView, UpdateSupplierView, DeleteSupplierView, GetSupplierView

urlpatterns = [
    path("create/", CreateSupplierView.as_view(), name="create-supplier"),
    path("list/", ListSupplierView.as_view(), name="list-supplier"),
    path("update/<int:pk>", UpdateSupplierView.as_view(), name="update-supplier"),
    path("delete/<int:pk>", DeleteSupplierView.as_view(), name="delete-supplier"),
    path("<int:pk>/", GetSupplierView.as_view(), name="get-supplier")
]
