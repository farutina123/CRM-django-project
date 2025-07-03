from django.urls import path
from .views import UserRegistrationView, AttachUserToCompanyView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("attach-user-to-company/", AttachUserToCompanyView.as_view(), name="attach_user")]


