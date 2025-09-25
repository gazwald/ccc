from __future__ import annotations

from typing import TYPE_CHECKING

from nicegui import app

from ccc.components.models.prompt import Prompt


def prompt_from_storage() -> Prompt:
    return Prompt(
        positive=app.storage.user.get("prompt_pos", "Cat with a hat"),
        negative=app.storage.user.get("prompt_neg", ""),
        seed=app.storage.user.get("seed"),
        steps=app.storage.user.get("steps"),
        cfg=app.storage.user.get("guidance_scale"),
        sampler_name=app.storage.user.get("sampler"),
        scheduler=app.storage.user.get("scheduler"),
    )
