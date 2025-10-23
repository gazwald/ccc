from __future__ import annotations

import click

from ccc.interface.main import run_interface
from ccc.models.enums import DatabaseState
from ccc.models.orm.db import init


@click.group()
def cli():
    pass


@cli.command()
def test():
    click.echo("Hello world")


@cli.command()
def db():
    _db()


def _db() -> DatabaseState:
    state, messages = init()
    for message in messages:
        click.echo(message)

    return state


@cli.command()
def interface():
    if _db() == DatabaseState.INITIALISED:
        run_interface(reload=False)
    else:
        click.echo("Database not fully initialised, skipping startup")


@cli.command()
def api():
    from fastapi import FastAPI

    from ccc.api.scheduler import router

    app = FastAPI()

    app.include_router(router)


if __name__ in {"__main__", "__mp_main__"}:
    run_interface(reload=True)
