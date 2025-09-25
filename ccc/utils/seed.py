import time
from functools import cache

from numpy import uint64
from numpy.random import Generator, default_rng

from ccc.constants import MAX_SEED


@cache
def _generator(seed: int | None = None) -> Generator:
    if seed is None:
        seed = time.time_ns()

    return default_rng(seed)


def generate_seed(generator: Generator | None = None) -> int:
    if generator is None:
        generator = default_rng()

    return int(generator.integers(low=0, high=MAX_SEED, dtype=uint64))
