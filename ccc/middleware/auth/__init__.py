from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app
from starlette.middleware.base import BaseHTTPMiddleware

from ccc.constants import UNRESTRICTED_PAGE_ROUTES


class AuthMiddleware(BaseHTTPMiddleware):
    """
    This middleware restricts access to all NiceGUI pages.

    It redirects the user to the login page if they are not authenticated.
    """

    async def dispatch(self, request: Request, call_next):
        if not app.storage.user.get("authenticated", False):
            if (
                not request.url.path.startswith("/_nicegui")
                and request.url.path not in UNRESTRICTED_PAGE_ROUTES
            ):
                return RedirectResponse(f"/login?redirect_to={request.url.path}")

        return await call_next(request)
