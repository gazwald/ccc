#!/usr/bin/env python
from nicegui import ui

from ccc.pages.index import index

ui.run(
    dark=True,
    storage_secret="hello world",
)
