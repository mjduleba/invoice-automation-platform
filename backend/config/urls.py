"""Root URL routes: Django admin, the versioned API, then the SPA for everything else."""

from django.contrib import admin
from django.urls import path, re_path

from apps.core.views import spa_index
from config.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
    # Any path outside backend-owned prefixes is an app route; the SPA's router handles it
    re_path(r"^(?!(?:api|admin|_allauth|static)(?:/|$)).*$", spa_index, name="spa"),
]
