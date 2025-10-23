from __future__ import annotations

from typing import TYPE_CHECKING

from ccc.components.endpoints import ComfyUI
from ccc.components.workflows.factory import workflow_factory
from ccc.config import app_config
from ccc.constants import DEFAULT_IMAGE
from ccc.utils.logger import logger

if TYPE_CHECKING:
    from PIL.Image import Image
    from PIL.ImageFile import ImageFile

    from ccc.models.config import Config
    from ccc.models.prompt import Prompt
    from ccc.models.workflow import Workflow, WorkflowState


class WorkflowHandler:
    config: Config
    workflow: Workflow
    state: WorkflowState
    image: Image | ImageFile = DEFAULT_IMAGE

    def __init__(
        self,
        workflow_name: str,
        client_id: str,
        prompt: Prompt,
        config: Config | None = None,
    ) -> None:
        logger.info(f"{self.__str__()} initialised with {client_id}, {workflow_name}")

        self.config = config or app_config()
        self.endpoint = ComfyUI(client_id, str(prompt.id), self.config)
        self.workflow = workflow_factory("txt2img", workflow_name, prompt)

        logger.info("Trigger...")
        self.trigger()
        logger.info("Wait...")
        self.wait()
        logger.info("Process...")
        self.process()

    def trigger(self):
        logger.info(self.workflow.prompt)
        self.endpoint.prompt(
            prompt=self.workflow.to_dict,
        )

    def wait(self):
        for state in self.endpoint.workflow_status():
            self.state = state
            if state.complete:
                return

    def process(self) -> None:
        self.image = self.endpoint.image(self.workflow.output) or DEFAULT_IMAGE
