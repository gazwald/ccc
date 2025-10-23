from __future__ import annotations

from time import time_ns

from pydantic.fields import Field
from pydantic.types import PositiveFloat, PositiveInt

from ccc.constants import MAX_CFG, MAX_SEED, MAX_STEPS
from ccc.models.base import BaseModel
from ccc.models.types import Sampler, Scheduler
from ccc.utils.seed import generate_seed


class Resolution(BaseModel):
    width: PositiveInt
    height: PositiveInt


class EmptyLatentImage(Resolution):
    pass


class LoadLatentImage(Resolution):
    pass


class Prompt(BaseModel):
    id: int = Field(default_factory=time_ns)
    positive: str
    negative: str
    seed: PositiveInt | None = Field(default_factory=generate_seed, ge=0, le=MAX_SEED)
    steps: PositiveInt = Field(default=20, ge=1, le=MAX_STEPS)
    cfg: PositiveFloat = Field(default=7, ge=0.0, le=MAX_CFG)
    sampler_name: Sampler = "euler"
    scheduler: Scheduler = "simple"
    denoise: PositiveFloat = Field(default=1.0, ge=0.1, le=1)

    width: PositiveInt = Field(default=512)
    height: PositiveInt = Field(default=512)

    @property
    def latent(self) -> EmptyLatentImage:
        return EmptyLatentImage(width=self.width, height=self.height)
