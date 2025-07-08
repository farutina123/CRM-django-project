from django.urls import path
from .views import CreateSupplierView

urlpatterns = [
    path("create/", CreateSupplierView.as_view(), name="create-supplier")
]
