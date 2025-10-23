from functools import cache

from ccc.models.config import Config


@cache
def app_config() -> Config:
    return Config()
