from django.urls import path
from .views import CreateStorageView, UpdateStorageView


urlpatterns = [
    path("create/", CreateStorageView.as_view(), name="create-storage"),
    path("update/<int:pk>/", UpdateStorageView.as_view(), name="update-storage")]
