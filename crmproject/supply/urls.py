from django.urls import path
from .views import CreateSupplyView


urlpatterns = [
    path("create/", CreateSupplyView.as_view(), name="create-supply")
    # path("list/", ListSupplierView.as_view(), name="list-supplier")
]