from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, cast

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ccc.config import app_config

if TYPE_CHECKING:
    from typing import Callable

ENGINE = create_engine(app_config().database.uri)
SESSION = sessionmaker(ENGINE)


def with_session[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapped(*args, **kwargs) -> R:
        _session = kwargs.get("session", SESSION)
        with _session.begin() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return wrapped


NewSession: Session = cast(Session, None)
