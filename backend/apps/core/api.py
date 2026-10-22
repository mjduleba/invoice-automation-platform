"""System endpoints that are not tied to a business resource."""

import logging
from typing import Literal

from django.db import DatabaseError, connection
from django.http import HttpRequest
from ninja import Router, Schema, Status

logger = logging.getLogger(__name__)

router = Router(tags=["system"])


class HealthOut(Schema):
    """Health check body; carries a status only, never data (NFR-08)."""

    status: Literal["ok", "error"]


@router.get(
    "/health",
    auth=None,
    response={200: HealthOut, 503: HealthOut},
    operation_id="health",
)
def health(request: HttpRequest) -> Status[HealthOut]:
    """Liveness and database check for the uptime monitor.

    Served at /api/v1/health, not /healthz: Cloud Run answers some paths ending in "z" itself.

    Args:
        request: incoming request; unused, public endpoint.

    Raises:
        None; database errors are caught and reported as 503.

    Returns:
        Status 200 with "ok" when the database answers, else 503 with "error".
    """
    # Round-trip a trivial query to prove the database connection works
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        logger.exception("Health check could not reach the database")
        return Status(503, HealthOut(status="error"))
    return Status(200, HealthOut(status="ok"))
