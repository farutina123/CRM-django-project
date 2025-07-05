from django.urls import path
from .views import CreateStorageView, UpdateStorageView, DeleteStorageView, GetStorageView


urlpatterns = [
    path("create/", CreateStorageView.as_view(), name="create-storage"),
    path("update/<int:pk>/", UpdateStorageView.as_view(), name="update-storage"),
    path("delete/<int:pk>/", DeleteStorageView.as_view(), name="delete-storage"),
    path("<int:pk>/", GetStorageView.as_view(), name="get-storage")]
