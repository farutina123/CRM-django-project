from django.urls import path
from .views import CreateStorageView


urlpatterns = [
    path("create-storage/", CreateStorageView.as_view(), name="create-storage")]
