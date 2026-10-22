import pytest
from django.db import connection

pytestmark = pytest.mark.django_db


def test_schema_extensions_are_installed() -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT extname FROM pg_extension WHERE extname IN ('pg_trgm', 'btree_gist')"
        )
        installed = {row[0] for row in cursor.fetchall()}

    assert installed == {"pg_trgm", "btree_gist"}
