#!/usr/bin/env python
from nicegui import app, ui

from ccc.components.auth import AuthMiddleware
from ccc.pages.index import index
from ccc.pages.login import login

app.add_middleware(AuthMiddleware)

ui.run(
    dark=True,
    title="Cursed Content Creator",
    favicon="🚀",
    storage_secret="hello world",
)
