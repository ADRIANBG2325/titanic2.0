"""
URLs principales del proyecto
"""

from django.contrib import admin
from django.urls import path, include
from predictor.views import index_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('predictor.urls')),
    path('', index_view, name='index'),
]

if settings.DEBUG:
    from django.views.static import serve
    from django.urls import re_path
    import os
    
    urlpatterns += [
        re_path(r'^frontend/(?P<path>.*)$', serve, {
            'document_root': os.path.join(settings.BASE_DIR, 'frontend'),
        }),
    ]
