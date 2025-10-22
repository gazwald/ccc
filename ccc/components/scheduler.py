"""
Scheduler is a priority queue that takes into account
the number of jobs that a user is currently running
and lowers their priority based on that.

TLDR: https://docs.python.org/3/library/heapq.html
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from heapq import heappop, heappush
from itertools import count
from time import sleep

from ccc.components.models.prompt import Prompt
from ccc.components.models.workflow import Workflow


class JobStatus(Enum):
    QUEUED = auto()
    PROCESSING = auto()
    DONE = auto()
    FAILED = auto()
    UNKNOWN = auto()


@dataclass(order=True)
class Job:
    priority: int = field(init=False)
    job_id: int
    prompt_id: int
    priority_offset: int
    user_id: int = field(compare=False)

    def __post_init__(self) -> None:
        self.priority = self.job_id + self.prompt_id + self.priority_offset

    def __hash__(self) -> int:
        return self.job_id


@dataclass
class JobDefinition:
    job_id: int
    user_id: int
    prompt: Prompt
    workflow: Workflow


class Scheduler:
    queue: list[Job]
    jobs_per_user: dict[int, int]
    jobs: set[Job]
    shutdown: bool = False

    def __init__(self) -> None:
        self.counter = count()
        self.queue = []
        self.jobs = set()
        self.jobs_per_user = {}

    def run(self):
        while not self.shutdown:
            self.process()
            sleep(1)

    def queue_size(self) -> int:
        return len(self.queue)

    def job_status(self, user_id: int, prompt_id: int) -> JobStatus:
        if any([job.user_id == user_id and job.prompt_id == prompt_id for job in self.queue]):
            return JobStatus.QUEUED
        if any([job.user_id == user_id and job.prompt_id == prompt_id for job in self.jobs]):
            return JobStatus.PROCESSING

        return self._job_status_from_api(user_id, prompt_id)

    def _job_status_from_api(self, user_id: int, prompt_id: int) -> JobStatus:
        raise NotImplementedError

    def enqueue(self, user_id: int, prompt_id: int):
        priority_offset: int = self._calculate_priority_offset(user_id)

        heappush(
            self.queue,
            Job(
                job_id=next(self.counter),
                prompt_id=prompt_id,
                priority_offset=priority_offset,
                user_id=user_id,
            ),
        )

    def _calculate_priority_offset(self, user_id: int) -> int:
        current_job_count: int = len([job for job in self.jobs if job.user_id == user_id])
        if current_job_count >= 1:
            self.jobs_per_user[user_id] = current_job_count + 1
            return self.jobs_per_user[user_id] + 1

        self.jobs_per_user[user_id] = 1
        return 0

    def _next_job(self) -> Job | None:
        if self.queue:
            job = heappop(self.queue)
            return job

    def process(self):
        job = self._next_job()
        if not job:
            return

        current_job_count = self.jobs_per_user[job.user_id]
        if current_job_count >= 1:
            self.jobs_per_user[job.user_id] = current_job_count - 1

        self.jobs.add(job)

        return job.user_id, job.prompt_id

    def _purge(self):
        self.__init__()
