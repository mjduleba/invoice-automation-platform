import logging
from typing import Literal

from django.db import DatabaseError, connection
from django.http import HttpRequest
from ninja import Router, Schema, Status

logger = logging.getLogger(__name__)

router = Router(tags=["system"])


class HealthOut(Schema):
    status: Literal["ok", "error"]


@router.get(
    "/health",
    auth=None,
    response={200: HealthOut, 503: HealthOut},
    operation_id="health",
)
def health(request: HttpRequest) -> Status[HealthOut]:
    """Liveness and database check for the uptime monitor; returns no data.

    Lives at /api/v1/health rather than /healthz because Cloud Run reserves
    some paths ending in "z" and answers /healthz itself.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        logger.exception("Health check could not reach the database")
        return Status(503, HealthOut(status="error"))
    return Status(200, HealthOut(status="ok"))
