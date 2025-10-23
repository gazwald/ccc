import click


@click.group()
def cli():
    pass


@cli.command()
def test():
    click.echo("Hello world")


@cli.command()
def interface():
    from nicegui import ui

    from ccc.interface.main import app

    ui.run(
        dark=True,
        title="Cursed Content Creator",
        favicon="🚀",
        storage_secret="hello world",
    )


@cli.command()
def api():
    from fastapi import FastAPI

    from ccc.api.scheduler import router

    app = FastAPI()

    app.include_router(router)
