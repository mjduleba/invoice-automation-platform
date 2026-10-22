import pytest
from django.db import DatabaseError
from django.test import Client

pytestmark = pytest.mark.django_db


def test_health_reports_ok_when_database_answers(client: Client) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_reports_503_when_database_fails(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    class BrokenConnection:
        def cursor(self) -> None:
            raise DatabaseError("connection refused")

    monkeypatch.setattr("apps.core.api.connection", BrokenConnection())

    response = client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json() == {"status": "error"}
