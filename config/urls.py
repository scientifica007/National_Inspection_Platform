"""Root URL configuration.

Presentation only: HTTP routing maps to per-app URL modules. No business rule
lives here.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin is a technical administration tool, not the product UI.
    path("admin/", admin.site.urls),
    path("", include("identity.urls")),
]
