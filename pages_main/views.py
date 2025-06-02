### views.py
from django.shortcuts import redirect
from django.http import Http404
from .models import StaticSiteUpload
import os
from django.conf import settings

def view_static_site(request, site_id):
    path = os.path.join(settings.MEDIA_ROOT, 'static_sites', str(site_id), 'index.html')
    print(path)
    if not os.path.exists(path):
        raise Http404("Site not found")
    return redirect(f'/media/static_sites/{site_id}/index.html')