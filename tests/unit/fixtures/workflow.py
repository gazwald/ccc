from __future__ import annotations

from typing import TYPE_CHECKING

from ccc.components.models.enums import NodeClassType as NCT
from ccc.components.models.workflow import Workflow
from ccc.components.workflows.nodes import noder

if TYPE_CHECKING:
    from typing import ClassVar


class MockWorkflow(Workflow):
    checkpoint: ClassVar[str] = "mock.safetensors"
    description = "Mock Workflow"
    base = "StableDiffusion1.5"

    @property
    def to_dict(self) -> dict:
        return {
            **noder(NCT.CheckpointLoaderSimple, self.checkpoint),
            **noder(NCT.CLIPTextEncode, self.prompt.positive, sentiment=True),
            **noder(NCT.CLIPTextEncode, self.prompt.negative, sentiment=False),
            **noder(NCT.KSampler, self.ksampler),
            **noder(NCT.VAEDecodeTiled),
            **noder(NCT.EmptyLatentImage, self.latent_empty),
            **noder(NCT.SaveImage),
        }

    @property
    def to_json(self) -> str:
        return "{'hello': 'world'}"
