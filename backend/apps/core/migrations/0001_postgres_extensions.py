"""Enable trusted Postgres extensions; the database owner can create them without superuser."""

from django.contrib.postgres.operations import BtreeGistExtension, TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    """Install pg_trgm and btree_gist."""

    initial = True

    dependencies = []

    operations = [
        TrigramExtension(),  # client search across name, address, email, phone (FR-002)
        BtreeGistExtension(),  # agreement exclusion constraint on overlapping dates (FR-005)
    ]
