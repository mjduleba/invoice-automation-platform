"""Tests for the public health endpoint."""

import pytest
from django.db import DatabaseError
from django.test import Client

pytestmark = pytest.mark.django_db


def test_health_reports_ok_when_database_answers(client: Client) -> None:
    """Health returns 200 "ok" with a working database.

    Args:
        client: Django test client.

    Raises:
        AssertionError: on an unexpected status or body.

    Returns:
        None.
    """
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_reports_503_when_database_fails(
    client: Client, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Health returns 503 "error" when the database query raises.

    Args:
        client: Django test client.
        monkeypatch: replaces the endpoint's database connection.

    Raises:
        AssertionError: on an unexpected status or body.

    Returns:
        None.
    """

    # Stand-in connection whose cursor always fails
    class BrokenConnection:
        def cursor(self) -> None:
            raise DatabaseError("connection refused")

    monkeypatch.setattr("apps.core.api.connection", BrokenConnection())

    response = client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json() == {"status": "error"}
