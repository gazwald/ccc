from __future__ import annotations

from datetime import timedelta
from pathlib import Path
from typing import TYPE_CHECKING, get_args

from PIL import Image

from ccc.components.models.base import Sampler, Scheduler

if TYPE_CHECKING:
    from typing import Final

DEFAULT_OUTPUT_PATH: Final[Path] = Path("output")
DEFAULT_WORKFLOW: Final[str] = "sdxl"
DEFAULT_WORKFLOW_TIMEOUT: Final[timedelta] = timedelta(minutes=3)
DEFAULT_IMAGE = Image.new(
    mode="RGB",
    size=(200, 200),
    color=(255, 153, 255),
)

MAX_SEED: Final[int] = 18446744073709551615  # uint64
MAX_STEPS: Final[int] = 80
MAX_CFG: Final[int] = 20

AVAILABLE_SCHEDULERS: Final[tuple[Scheduler, ...]] = get_args(Scheduler)
AVAILABLE_SAMPLERS: Final[tuple[Sampler, ...]] = get_args(Sampler)
