from typing import cast

from nicegui import app, run, ui
from nicegui.binding import BindableProperty
from nicegui.elements.button import Button
from nicegui.elements.grid import Grid

from ccc.components.handler import WorkflowHandler
from ccc.components.workflows.factory import AVAILABLE_WORKFLOWS, workflow_factory
from ccc.constants import AVAILABLE_SAMPLERS, AVAILABLE_SCHEDULERS, DEFAULT_IMAGE, DEFAULT_WORKFLOW
from ccc.interface.parts.menu import menu
from ccc.models.base import Sampler, Scheduler
from ccc.models.prompt import Prompt
from ccc.models.workflow import Workflow
from ccc.utils.logger import logger
from ccc.utils.seed import generate_seed


def _randomise_seed():
    if app.storage.user.get("randomise_seed", True):
        app.storage.user["seed"] = generate_seed()


def _toggle_random_seed():
    if app.storage.user.get("randomise_seed", True):
        app.storage.user["randomise_seed"] = True


def _workflow_update() -> None:
    workflow_name: str | None = app.storage.user.get("workflow")
    if workflow_name is None or workflow_name not in AVAILABLE_WORKFLOWS:
        workflow_name = DEFAULT_WORKFLOW
        app.storage.user["workflow"] = workflow_name

    workflow: type[Workflow] = workflow_factory("txt2img", workflow_name, None)
    app.storage.user["steps"] = workflow.defaults["steps"]
    app.storage.user["scheduler"] = workflow.defaults["scheduler"]
    app.storage.user["sampler"] = workflow.defaults["sampler"]
    app.storage.user["guidance"] = workflow.defaults["guidance"]
    app.storage.user["steps"] = workflow.defaults["steps"]
    _sidebar.refresh()


def _prompt() -> Prompt:
    steps = cast(int, app.storage.user["steps"])
    cfg = cast(int, app.storage.user["guidance"])
    sampler_name = cast(Sampler, app.storage.user["sampler"])
    scheduler = cast(Scheduler, app.storage.user["scheduler"])

    return Prompt(
        positive=app.storage.user["prompt_pos"],
        negative=app.storage.user["prompt_neg"],
        seed=app.storage.user.get("seed", generate_seed()),
        steps=steps,
        cfg=cfg,
        sampler_name=sampler_name,
        scheduler=scheduler,
    )


@ui.refreshable
def _sidebar():
    if not app.storage.user.get("workflow"):
        _workflow_update()

    with ui.column():
        ui.select(
            label="Workflow",
            options=AVAILABLE_WORKFLOWS,
            value=DEFAULT_WORKFLOW,
            on_change=_workflow_update,
        ).bind_value(app.storage.user, "workflow")

        ui.textarea(
            label="Positive",
            placeholder="Cat with a hat",
        ).bind_value(app.storage.user, "prompt_pos")
        ui.textarea(
            label="Negative",
            placeholder="text, watermark",
        ).bind_value(app.storage.user, "prompt_neg")

        with ui.expansion("Advanced") as advanced:
            ui.number(
                label="Seed",
                precision=0,
            ).bind_value(app.storage.user, "seed")

            ui.radio({1: "Random", 2: "Fixed"}, value=1).props("inline")
            ui.button("Fixed", on_click=_randomise_seed)
            # ui.button("Random", on_click=_randomise_seed)
            ui.number(
                label="Steps",
                precision=0,
            ).bind_value(app.storage.user, "steps")
            ui.number(
                label="Guidance",
                value=5,
                precision=1,
            ).bind_value(app.storage.user, "guidance")
            ui.select(
                label="Scheduler",
                options=list(AVAILABLE_SCHEDULERS),
            ).bind_value(app.storage.user, "scheduler")
            ui.select(
                label="Sampler",
                options=list(AVAILABLE_SAMPLERS),
            ).bind_value(app.storage.user, "sampler")
        # ui.switch("Show Advanced", on_change=lambda: advanced.set_value(not advanced.value))


class Gen:
    """
    We'll need to queue these requests - probably in the database?
    """

    generating = BindableProperty()
    image = BindableProperty()
    workflow_handler: WorkflowHandler
    workflow_name: str
    user_id: str
    prompt: Prompt
    endpoint_available: bool = False

    def __init__(self) -> None:
        self.image = DEFAULT_IMAGE
        self.timer = ui.timer(5, self._endpoint_check)

    async def generate(
        self,
        user_id: str,
        workflow_name: str,
        prompt: Prompt,
        button: Button,
    ):
        logger.info(f"{self.__str__()}.generate called with {user_id}, {workflow_name}")
        self.user_id = user_id
        self.workflow_name = workflow_name
        self.prompt = prompt
        button.disable()
        await run.io_bound(self._generate)
        self.image = self.workflow_handler.image
        button.enable()
        _main.refresh()

    def _generate(self):
        self.workflow_handler = WorkflowHandler(
            workflow_name=self.workflow_name,
            client_id=self.user_id,
            prompt=self.prompt,
        )

    def _endpoint_check(self): ...


@ui.refreshable
def _main(gen):
    with ui.column():
        ui.image(gen.image).bind_source(gen.image)
        ui.button(
            "Generate",
            on_click=lambda e: gen.generate(
                app.storage.browser["id"],
                app.storage.user["workflow"],
                _prompt(),
                e.sender,
            ),
        )
        ui.button("Download", on_click=lambda: ui.download.content(gen.image, "image.png"))


@ui.page("/")
def index() -> Grid:
    gen = Gen()
    with ui.grid(columns=2) as index:
        _sidebar()
        _main(gen)

    menu()

    return index
