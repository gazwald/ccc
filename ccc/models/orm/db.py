from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING, cast

from sqlalchemy import create_engine
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session, sessionmaker

from ccc.config import app_config
from ccc.models.enums import DatabaseState
from ccc.models.orm.tables import Base, Image, Prompt, User

if TYPE_CHECKING:
    from typing import Callable

ENGINE = create_engine(app_config().database.uri)
SESSION = sessionmaker(ENGINE)
NewSession: Session = cast(Session, None)


def with_session[**P, R](func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapped(*args, **kwargs) -> R:
        _session = kwargs.get("session", SESSION)
        with _session.begin() as session:
            kwargs["session"] = session
            return func(*args, **kwargs)

    return wrapped


def init() -> tuple[DatabaseState, list[str]]:
    state: DatabaseState = check()
    messages: list[str] = []
    match state:
        case DatabaseState.NOT_INITIALISED:
            messages.append("Initialsing database now...")
            Base.metadata.create_all(ENGINE)
            messages.append("Database initialsed")
        case DatabaseState.PARTIAL:
            messages.append("Eh? Partially initialsed DB")
        case DatabaseState.INITIALISED:
            messages.append("Database looks initialsed, skipping initialisation")

    return check(), messages


def check() -> DatabaseState:
    engine_inspect = inspect(ENGINE)
    table_state: list[bool] = [
        engine_inspect.has_table(table.__tablename__) for table in (Image, Prompt, User)
    ]

    if all(table_state):
        return DatabaseState.INITIALISED
    if any(table_state):
        return DatabaseState.PARTIAL

    return DatabaseState.NOT_INITIALISED
