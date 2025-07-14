from django.urls import path
from .views import UserRegistrationView, AttachUserToCompanyView, ListGetUserView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("attach-user-to-company/", AttachUserToCompanyView.as_view(), name="attach_user"),
    path("list_user/", ListGetUserView.as_view(), name="list-user")
]


