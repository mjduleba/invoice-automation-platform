"""Enable the extensions the schema depends on.

pg_trgm backs client search (FR-002); btree_gist backs the agreement
exclusion constraint (FR-005). Both are trusted extensions, so the database
owner can create them without superuser rights.
"""

from django.contrib.postgres.operations import BtreeGistExtension, TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        TrigramExtension(),
        BtreeGistExtension(),
    ]
