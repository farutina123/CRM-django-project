from django.contrib import admin
from . import models


@admin.register(models.Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ["address"]
