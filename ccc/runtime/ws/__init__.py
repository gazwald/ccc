from __future__ import annotations

from functools import wraps
from typing import cast

from websockets.sync.client import ClientConnection, connect

from ccc.config import app_config

# async def with_websocket(config: Config, client_id: UUID4) -> AsyncGenerator[ClientConnection]:
#     async with connect(config.connection.uri_ws(client_id)) as websocket:
#         yield websocket


def with_connection(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "connection" in kwargs:
            return f(*args, **kwargs)
        if "config" in kwargs:
            config = kwargs["config"]
        else:
            config = app_config()

        if "client_id" in kwargs:
            uri = config.connection.uri_ws(kwargs["client_id"])
        else:
            raise NotImplementedError("What do?")

        with connect(uri) as connection:
            return f(*args, connection=connection, **kwargs)

    return wrapper


NEW_CONNECTION: ClientConnection = cast(ClientConnection, None)
