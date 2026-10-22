"""Tests for database setup the schema depends on."""

import pytest
from django.db import connection

pytestmark = pytest.mark.django_db


def test_schema_extensions_are_installed() -> None:
    """Migrations install pg_trgm and btree_gist.

    Args:
        None.

    Raises:
        AssertionError: when either extension is missing.

    Returns:
        None.
    """
    # Read installed extensions straight from the Postgres catalog
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT extname FROM pg_extension WHERE extname IN ('pg_trgm', 'btree_gist')"
        )
        installed = {row[0] for row in cursor.fetchall()}

    assert installed == {"pg_trgm", "btree_gist"}
