import reflex as rx

config = rx.Config(
    app_name="ccc",
    telemetry_enabled=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
