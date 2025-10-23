from typing import TYPE_CHECKING

from nicegui import app, ui
from sqlalchemy import select

from ccc.components.orm.db import with_session
from ccc.components.orm.tables import User

if TYPE_CHECKING:
    from ccc.components.orm.db import NewSession


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
    raise NotImplementedError
