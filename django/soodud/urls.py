"""soodud URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from decouple import config


urlpatterns = [
    path(f'{config("DJANGO_ADMIN_SITE_PATH", default="admin")}/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest')),
]
