"""Tests for serving the built SPA through Django and WhiteNoise."""

from pathlib import Path

import pytest
from django.http import FileResponse
from django.test import Client
from pytest_django.fixtures import Settings

INDEX_HTML = "<!doctype html><title>Invoicing</title>"
HASHED_ASSET = "_app/immutable/entry/app.Bk3x9QzA.js"


@pytest.fixture
def frontend_build(tmp_path: Path, settings: Settings) -> Path:
    """Fake SvelteKit build with index.html and one hashed asset, wired into settings.

    Args:
        tmp_path: per-test temporary directory.
        settings: pytest-django settings override.

    Raises:
        None.

    Returns:
        Path to the fake build directory.
    """
    # Minimal build layout matching adapter-static output
    (tmp_path / "index.html").write_text(INDEX_HTML)
    asset_path = tmp_path / HASHED_ASSET
    asset_path.parent.mkdir(parents=True)
    asset_path.write_text("console.log('app');")

    # View reads FRONTEND_BUILD_DIR per request; WhiteNoise reads its root when the client starts
    settings.FRONTEND_BUILD_DIR = tmp_path
    settings.WHITENOISE_ROOT = tmp_path
    return tmp_path


@pytest.mark.usefixtures("frontend_build")
@pytest.mark.parametrize("path", ["/", "/log", "/storms/new", "/clients/42"])
def test_app_routes_serve_index_html(client: Client, path: str) -> None:
    """Every app route returns index.html so the SPA router can take over.

    Args:
        client: Django test client.
        path: frontend route to request.

    Raises:
        AssertionError: when the route does not serve index.html uncached.

    Returns:
        None.
    """
    response = client.get(path)

    assert response.status_code == 200
    assert response.content.decode() == INDEX_HTML
    assert response["Cache-Control"] == "no-cache"
    assert "csrftoken" in response.cookies


# close() fires request_finished, which checks the database connection
@pytest.mark.django_db
@pytest.mark.usefixtures("frontend_build")
def test_hashed_assets_are_served_with_long_cache(client: Client) -> None:
    """WhiteNoise serves SvelteKit's immutable bundles with a far-future cache header.

    Args:
        client: Django test client.

    Raises:
        AssertionError: when the asset is missing or not marked immutable.

    Returns:
        None.
    """
    response = client.get(f"/{HASHED_ASSET}")
    # WhiteNoise streams the file; read it, then close the response to release the handle
    assert isinstance(response, FileResponse)
    body = response.getvalue()
    response.close()

    assert response.status_code == 200
    assert body == b"console.log('app');"
    assert "immutable" in response["Cache-Control"]


@pytest.mark.django_db
@pytest.mark.usefixtures("frontend_build")
def test_unknown_api_paths_are_404_not_the_spa(client: Client) -> None:
    """A typo under /api/ fails loudly instead of returning the app shell.

    Args:
        client: Django test client.

    Raises:
        AssertionError: when the SPA answers an API path.

    Returns:
        None.
    """
    response = client.get("/api/v1/does-not-exist")

    assert response.status_code == 404
    assert INDEX_HTML not in response.content.decode()


@pytest.mark.usefixtures("frontend_build")
def test_admin_without_slash_still_redirects_to_admin(client: Client) -> None:
    """/admin is backend-owned; Django's slash redirect wins over the SPA.

    Args:
        client: Django test client.

    Raises:
        AssertionError: when /admin is served by the SPA.

    Returns:
        None.
    """
    response = client.get("/admin")

    assert response.status_code == 301
    assert response["Location"] == "/admin/"


@pytest.mark.usefixtures("frontend_build")
def test_spa_rejects_writes(client: Client) -> None:
    """The SPA view only answers GET and HEAD.

    Args:
        client: Django test client.

    Raises:
        AssertionError: when a POST is accepted.

    Returns:
        None.
    """
    response = client.post("/log")

    assert response.status_code == 405


def test_app_routes_404_without_a_build(client: Client, tmp_path: Path, settings: Settings) -> None:
    """Without a frontend build (local dev uses Vite), app routes are 404.

    Args:
        client: Django test client.
        tmp_path: empty directory standing in for a missing build.
        settings: pytest-django settings override.

    Raises:
        AssertionError: when a route returns anything but 404.

    Returns:
        None.
    """
    settings.FRONTEND_BUILD_DIR = tmp_path

    response = client.get("/log")

    assert response.status_code == 404
