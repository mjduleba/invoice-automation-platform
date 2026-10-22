"""Shared pytest fixtures."""

import pytest
from pytest_django.fixtures import Settings


@pytest.fixture(autouse=True)
def plain_static_storage(settings: Settings) -> None:
    """Use unhashed static names; tests run without collectstatic, so no manifest exists.

    Args:
        settings: pytest-django settings override.

    Raises:
        None.

    Returns:
        None.
    """
    settings.STORAGES = {
        **settings.STORAGES,
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
