from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pytest

from ccc.components.scheduler import Scheduler

if TYPE_CHECKING:
    from typing import Literal

    from _pytest.mark.structures import ParameterSet

pytestmark = pytest.mark.scheduler


@dataclass
class Scenario:
    setup: list[tuple[Literal["enqueue"], int, int] | tuple[Literal["process"], None, None]]
    expected: list[tuple[int, int]]
    test_id: str
    description: str | None = None

    def as_param(self) -> ParameterSet:
        return pytest.param(self, id=self.test_id)


scenarios = [
    Scenario(
        setup=[],
        expected=[],
        description="Nothing in, nothing out",
        test_id="NothingInNothingOut",
    ),
    Scenario(
        setup=[
            ("enqueue", 1, 1),
            ("process", None, None),
        ],
        expected=[(1, 1)],
        description="Single job in, single job out",
        test_id="SingleInSingleOut",
    ),
    Scenario(
        setup=[
            ("enqueue", 1, 1),
            ("process", None, None),
            ("enqueue", 1, 2),
            ("enqueue", 2, 3),
            ("process", None, None),
            ("process", None, None),
        ],
        expected=[(1, 1), (2, 3), (1, 2)],
        description=(
            "Single job in, start processing the first job."
            "During processing the first job two new jobs come in."
            "One job from the first user, and another job from a second user."
            "The user whose job currently isn't being processed has priority."
        ),
        test_id="MultipleInFairOut",
    ),
    Scenario(
        setup=[
            ("enqueue", 1, 1),
            ("process", None, None),
            ("enqueue", 1, 2),
            ("enqueue", 2, 3),
            ("process", None, None),
            ("process", None, None),
            ("enqueue", 3, 4),
            ("enqueue", 2, 5),
            ("enqueue", 4, 6),
            ("enqueue", 2, 7),
            ("process", None, None),
            ("process", None, None),
            ("process", None, None),
            ("process", None, None),
        ],
        expected=[(1, 1), (2, 3), (1, 2), (3, 4), (4, 6), (2, 5), (2, 7)],
        test_id="MultipleInFairOutExtended",
    ),
]


@pytest.fixture
def scheduler() -> Scheduler:
    return Scheduler()


@pytest.mark.parametrize(
    ("scenario"),
    [scenario.as_param() for scenario in scenarios],
)
def test_schedule(scheduler: Scheduler, scenario: Scenario):
    actual = []
    for step in scenario.setup:
        action, user_id, prompt_id = step
        match action:
            case "enqueue":
                scheduler.enqueue(user_id, prompt_id)
            case "process":
                actual.append(scheduler.process())

    assert actual == scenario.expected
