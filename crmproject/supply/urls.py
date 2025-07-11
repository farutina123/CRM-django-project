from django.urls import path
from .views import CreateSupplyView, ListGetSupplyView


urlpatterns = [
    path("create/", CreateSupplyView.as_view(), name="create-supply"),
    path("list/", ListGetSupplyView.as_view(), name="list-supply")
]