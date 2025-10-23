from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import timedelta
from enum import Enum, auto
from typing import TYPE_CHECKING, TypedDict

from ccc.models.base import BaseModel, Sampler, Scheduler
from ccc.models.enums import NodeID
from ccc.models.prompt import Prompt
from ccc.models.types import DiffussionModel, KSampler, LatentEmpty, LatentImage

if TYPE_CHECKING:
    from typing import ClassVar


class WorkflowStatus(Enum):
    executing = auto()
    progress = auto()
    status = auto()
    unknown = auto()


class WorkflowState(BaseModel):
    progress: int = 0
    total: int = 0
    complete: bool = False
    status: WorkflowStatus = WorkflowStatus.unknown


class WorkflowDefaults(TypedDict):
    steps: int
    guidance: int
    width: int
    height: int
    scheduler: Scheduler
    sampler: Sampler


class Workflow(BaseModel, ABC):
    checkpoint: ClassVar[str]
    description: ClassVar[str]
    base: ClassVar[DiffussionModel]
    output: ClassVar[NodeID]
    defaults: ClassVar[WorkflowDefaults]
    prompt: Prompt
    timeout: timedelta | None = None

    @property
    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError

    @property
    @abstractmethod
    def to_json(self) -> str:
        raise NotImplementedError

    @property
    def ksampler(self) -> KSampler:
        if TYPE_CHECKING:
            assert self.prompt.seed is not None

        return KSampler(
            {
                "seed": self.prompt.seed,
                "steps": self.prompt.steps,
                "cfg": self.prompt.cfg,
                "sampler_name": self.prompt.sampler_name,
                "scheduler": self.prompt.scheduler,
                "denoise": self.prompt.denoise,
            }
        )

    @property
    def latent_empty(self) -> LatentEmpty:
        return LatentEmpty(
            {
                "width": self.prompt.latent.width,
                "height": self.prompt.latent.height,
                "batch_size": 1,
            }
        )

    @property
    def latent_image(self) -> LatentImage:
        return LatentImage(
            {
                "image": "blah",
            }
        )
