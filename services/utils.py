import time
from collections.abc import Collection
from typing import Generator, TypeVar

T = TypeVar('T')


def batched(lst: Collection, n: int) -> Generator:
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def timestamp_ms() -> int:
    return int(time.time() * 1000)
