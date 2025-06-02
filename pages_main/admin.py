### admin.py
from django.contrib import admin
from .models import StaticSiteUpload

@admin.register(StaticSiteUpload)
class StaticSiteUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'zip_file', 'uploaded_at')