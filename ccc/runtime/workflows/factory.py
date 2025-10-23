from __future__ import annotations

from typing import TYPE_CHECKING, overload

from ccc.models.base import WorkflowType
from ccc.models.prompt import Prompt
from ccc.models.workflow import Workflow
from ccc.runtime.workflows.txt2img.sd15 import StableDiffusion
from ccc.utils.logger import logger

if TYPE_CHECKING:
    from typing import Final

WORKFLOWS: dict[
    WorkflowType,
    dict[str, type[Workflow]],
] = {
    "txt2img": {"sd": StableDiffusion},
}
AVAILABLE_WORKFLOWS: Final[dict[str, str]] = {
    key: workflow.description for key, workflow in WORKFLOWS["txt2img"].items()
}


@overload
def workflow_factory(
    workflow_type: WorkflowType,
    workflow_name: str,
    prompt: Prompt,
) -> Workflow: ...
@overload
def workflow_factory(
    workflow_type: WorkflowType,
    workflow_name: str,
    prompt: None,
) -> type[Workflow]: ...
def workflow_factory(workflow_type, workflow_name, prompt):
    logger.info(f"workflow_factory called with {workflow_type} {workflow_name}")
    if workflow_type not in WORKFLOWS:
        raise Exception(f"Workflow type {workflow_type} not in workflow factory")
    if workflow_name not in WORKFLOWS[workflow_type]:
        raise Exception(f"Workflow name {workflow_name} not in workflow factory")

    if prompt:
        return WORKFLOWS[workflow_type][workflow_name](prompt=prompt)

    return WORKFLOWS[workflow_type][workflow_name]


def workflows_as_tuple(workflow_type: WorkflowType) -> tuple[str, ...]:
    return tuple(WORKFLOWS[workflow_type].keys())
