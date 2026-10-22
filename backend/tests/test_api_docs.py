import pytest
from django.contrib.auth.models import User
from django.test import Client

pytestmark = pytest.mark.django_db


def test_api_docs_redirect_anonymous_users_to_login(client: Client) -> None:
    response = client.get("/api/v1/docs")

    assert response.status_code == 302
    assert response["Location"].startswith("/admin/login/")


def test_api_docs_open_for_staff(client: Client, admin_user: User) -> None:
    client.force_login(admin_user)

    response = client.get("/api/v1/docs")

    assert response.status_code == 200


def test_openapi_schema_lists_the_health_endpoint(client: Client, admin_user: User) -> None:
    client.force_login(admin_user)

    schema = client.get("/api/v1/openapi.json").json()

    assert "/api/v1/health" in schema["paths"]
