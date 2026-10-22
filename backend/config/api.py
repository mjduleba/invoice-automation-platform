"""Versioned JSON API mounted at /api/v1; its OpenAPI schema generates the frontend client."""

from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI

from apps.core.api import router as core_router

# Docs and schema are Admin only; staff stands in until M2 adds roles
api = NinjaAPI(
    title="Invoicing API",
    version="1",
    docs_decorator=staff_member_required,
)

# Routers, one per app
api.add_router("", core_router)
