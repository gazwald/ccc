from typing import Generator

import pytest

from ccc.components.handler import WorkflowHandler
from ccc.components.models.config import Config
from ccc.components.models.prompt import Prompt
from tests.unit.fixtures.workflow import MockWorkflow


@pytest.fixture
def default_config() -> Generator[Config, None, None]:
    yield Config()


@pytest.fixture
def default_prompt() -> Generator[Prompt, None, None]:
    yield Prompt(
        id=1,
        positive="cat with a hat",
        negative="hands",
        seed=42,
    )


@pytest.fixture
def default_workflow(default_prompt) -> Generator[MockWorkflow, None, None]:
    yield MockWorkflow(prompt=default_prompt)


@pytest.fixture
def default_workflowhandler(
    default_client_id,
    default_config,
    default_workflow,
    default_prompt,
) -> Generator[WorkflowHandler, None, None]:
    yield WorkflowHandler(
        client_id=default_client_id,
        config=default_config,
        workflow_name=default_workflow,
        prompt=default_prompt,
    )
