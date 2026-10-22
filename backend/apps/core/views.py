"""Views that serve the Svelte single-page app."""

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_safe


@require_safe
@ensure_csrf_cookie
def spa_index(request: HttpRequest) -> HttpResponse:
    """Serve the SPA's index.html for any app route, e.g. /log or /storms/new.

    Args:
        request: GET or HEAD request for a frontend route.

    Raises:
        Http404: when no frontend build is present (local dev uses the Vite server instead).

    Returns:
        index.html, never cached, with the csrftoken cookie the API client sends back on writes.
    """
    index_file = settings.FRONTEND_BUILD_DIR / "index.html"
    if not index_file.is_file():
        raise Http404("Frontend build not found")

    # index.html names the current hashed bundles, so browsers must revalidate it every time
    response = HttpResponse(index_file.read_bytes(), content_type="text/html; charset=utf-8")
    response["Cache-Control"] = "no-cache"
    return response
