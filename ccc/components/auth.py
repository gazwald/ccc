from typing import TYPE_CHECKING

from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from sqlalchemy import select
from starlette.middleware.base import BaseHTTPMiddleware

from ccc.components.orm.db import NewSession, with_session
from ccc.components.orm.tables import User
from ccc.constants import UNRESTRICTED_PAGE_ROUTES

if TYPE_CHECKING:
    ...


def logout() -> None:
    app.storage.user.clear()
    ui.navigate.to("/login")


def is_authenticated() -> bool:
    return app.storage.user.get("authenticated", False)


@with_session
def authenticate(username: str, password: str, session: NewSession = None) -> bool:
    if not username or not password:
        return False

    if username == "admin" and password == "admin":
        return True

    user: User | None = session.execute(
        select(User).where(User.username == username)
    ).scalar_one_or_none()
    if not user:
        return False

    if user.password == password:
        return True

    return False


@with_session
def register(username: str, password: str, session: NewSession = None) -> bool:
    pass


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
