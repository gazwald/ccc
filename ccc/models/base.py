from typing import Literal, TypedDict

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel): ...


WorkflowType = Literal[
    "txt2img",
    "img2img",
]
Sampler = Literal[
    "dpmpp_3m_sde_gpu",
    "euler",
    "euler_ancestral",
]
Scheduler = Literal[
    "beta",
    "ddim_uniform",
    "exponential",
    "karras",
    "kl_optimal",
    "linear_quadratic",
    "normal",
    "sgm_uniform",
    "simple",
]
DiffussionModel = Literal[
    "StableDiffusion1.5",
    "StableDiffusion3.5",
    "StableDiffusionXL",
    "Flux",
    "HiDream",
]
NodeClassType = Literal[
    "CLIPTextEncode",
    "CheckpointLoaderSimple",
    "EmptyLatentImage",
    "KSampler",
    "LoadImage",
    "SaveImage",
    "VAEDecodeTiled",
    "VAEEncodeTiled",
    "VAELoader",
]


class KSampler(TypedDict):
    seed: int
    steps: int
    cfg: float
    sampler_name: Sampler
    scheduler: Scheduler
    denoise: float


class LatentEmpty(TypedDict):
    width: int
    height: int
    batch_size: int


class LatentImage(TypedDict):
    image: str
