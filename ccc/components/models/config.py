from pathlib import Path
from typing import Literal

from pydantic.types import PositiveFloat, PositiveInt

from ccc.components.models.base import BaseModel


class DatabaseConfig(BaseModel):
    scheme: Literal["sqlite", "postgres"] = "sqlite"
    filename: Literal["ccc.db", ":memory:"] = "ccc.db"

    @property
    def path(self) -> Path:
        return Path(self.filename)

    @property
    def uri(self) -> str:
        return f"{self.scheme}:///{self.filename}"


class ConnectionConfig(BaseModel):
    host: str = "127.0.0.1"
    port: PositiveInt = 8188
    sleep: PositiveFloat | None = 0.1
    queue: str = "default-queue"
    concurrency: PositiveInt = 1

    # def uri_ws(self, client_id: str) -> str:
    #     return f"ws://{self.host}:{self.port}/ws?clientId={client_id}"

    @property
    def uri_ws(self) -> str:
        return f"ws://{self.host}:{self.port}/ws"

    @property
    def uri_http(self) -> str:
        return f"http://{self.host}:{self.port}"


class Config(BaseModel):
    database: DatabaseConfig = DatabaseConfig()
    connection: ConnectionConfig = ConnectionConfig()
