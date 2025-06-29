from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from . import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username"]

