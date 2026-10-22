"""App config for core: system endpoints and shared database setup."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Registers the core app under the short label "core"."""

    name = "apps.core"
    label = "core"
