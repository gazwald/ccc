from nicegui import ui

from ccc.components.auth import is_authenticated, logout


def menu():
    with ui.page_sticky(position="top-right"):
        with ui.button(icon="menu"):
            with ui.menu().props("auto-close"):
                ui.menu_item("Help")

                if is_authenticated():
                    ui.menu_item("Profile")
                    ui.menu_item("Logout", on_click=logout)
                else:
                    ui.menu_item("Login")
