### urls.py
from django.urls import path
from .views import view_static_site
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('site/<int:site_id>/', view_static_site, name='view_static_site'),
] + static('/media/', document_root=settings.MEDIA_ROOT)