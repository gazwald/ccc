from fastapi.responses import RedirectResponse
from nicegui import app, ui

from ccc.components.auth import authenticate


@ui.page("/login")
def login(redirect_to: str = "/") -> RedirectResponse | None:
    def try_login() -> None:  # local function to avoid passing username and password as arguments
        if authenticate(username.value, password.value):
            app.storage.user.update({"username": username.value, "authenticated": True})
            ui.navigate.to(redirect_to)  # go back to where the user wanted to go
        else:
            ui.notify("Wrong username or password", color="negative")

    if app.storage.user.get("authenticated", False):
        return RedirectResponse("/")

    with ui.card().classes("absolute-center"):
        username = ui.input("Username").on(
            "keydown.enter",
            try_login,
        )
        password = ui.input(
            "Password",
            password=True,
            password_toggle_button=True,
        ).on(
            "keydown.enter",
            try_login,
        )
        ui.button("Log in", on_click=try_login)

    return None
