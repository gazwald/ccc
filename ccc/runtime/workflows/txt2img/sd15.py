import json

from ccc.models.enums import NodeClassType as NCT
from ccc.models.enums import NodeID
from ccc.models.workflow import Workflow, WorkflowDefaults
from ccc.runtime.workflows.nodes import noder


class StableDiffusion(Workflow):
    checkpoint = "v1-5-pruned-emaonly-fp16.safetensors"
    description = "Stable Diffusion"
    base = "StableDiffusion1.5"
    output = NodeID.save_image_id
    defaults = WorkflowDefaults(
        steps=20,
        guidance=8,
        width=512,
        height=512,
        scheduler="simple",
        sampler="euler",
    )

    @property
    def to_dict(self) -> dict:
        return {
            **noder(NCT.EmptyLatentImage, self.latent_empty),
            **noder(NCT.CheckpointLoaderSimple, self.checkpoint),
            **noder(NCT.CLIPTextEncode, self.prompt.positive, sentiment=True),
            **noder(NCT.CLIPTextEncode, self.prompt.negative, sentiment=False),
            **noder(NCT.KSampler, self.ksampler),
            **noder(NCT.VAEDecodeTiled),
            **noder(NCT.SaveImage),
        }

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)
