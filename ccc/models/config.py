from pathlib import Path
from typing import Literal

from pydantic.types import PositiveFloat, PositiveInt

from ccc.models.base import BaseModel


class DatabaseConfig(BaseModel):
    scheme: Literal["sqlite", "postgres"] = "sqlite"
    host: str = "127.0.0.1"
    port: PositiveInt = 5432
    database: str = "ccc"
    username: str = "ccc"
    password: str = "password"

    @property
    def path(self) -> Path:
        return Path(f"{self.database}.db")

    @property
    def uri(self) -> str:
        match self.scheme:
            case "sqlite":
                return f"{self.scheme}:///{self.path}"
            case "postgres":
                return (
                    f"{self.scheme}://"
                    f"{self.username}:{self.password}"
                    "@"
                    f"{self.host}:{self.port}/{self.database}"
                )


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
