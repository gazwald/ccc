#!/usr/bin/env python
from nicegui import app, ui

from ccc.interface.pages.index import index
from ccc.interface.pages.login import login
from ccc.middleware.auth import AuthMiddleware

app.add_middleware(AuthMiddleware)

ui.run(
    dark=True,
    title="Cursed Content Creator",
    favicon="🚀",
    storage_secret="hello world",
)
