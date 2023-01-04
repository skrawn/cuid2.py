import os
from math import ceil

from tests import create_id_pool


def test_collision() -> None:
    magic: int = 750000
    workers: int = min(32, (os.cpu_count() or 1) + 4)
    id_pool: tuple[list[str], list[int], list[int]] = create_id_pool(magic)

    pooled_ids: list[str] = id_pool[0]
    id_set: set[str] = set(pooled_ids)
    histogram: list[int] = id_pool[2]

    expected_bin_size: int = ceil(magic / workers / len(histogram))
    tolerance: float = 0.05

    max_bin_size = round(expected_bin_size * (1 + tolerance))
    min_bin_size = round(expected_bin_size * (1 - tolerance))

    assert len(id_set) == magic  # noqa
    assert all(x > min_bin_size and x < max_bin_size for x in histogram)  # noqa
