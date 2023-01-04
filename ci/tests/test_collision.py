import os
from concurrent.futures import Future, ThreadPoolExecutor
from math import ceil

import pytest
from ci.tests import create_id_pool


async def worker(max) -> tuple[list[int], list[int], list[int]]:
    return await create_id_pool(max)


@pytest.mark.asyncio
async def test_collision() -> None:
    magic: int = 1000000
    workers: int = min(32, os.cpu_count() or 1 + 4)
    id_pools: list[tuple[list[int], list[int], list[int]]] = []

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future: Future = executor.submit(worker, int(magic / workers))
        result: tuple[list[int], list[int], list[int]] = await future.result()
        id_pools.append(result)

    pooled_ids: list[int] = [id for pool in id_pools for id in pool[0]]
    id_samples: list[int] = pooled_ids[0:10]
    id_sample_set: set[int] = set(id_samples)
    histogram: list[int] = id_pools[0][2]

    expected_bin_size: int = ceil(magic / workers / len(histogram))
    tolerance: float = 0.05

    max_bin_size = round(expected_bin_size * (1 + tolerance))
    min_bin_size = round(expected_bin_size * (1 - tolerance))

    assert len(id_sample_set) == magic  # noqa
    assert all(x > min_bin_size and x < max_bin_size for x in histogram)  # noqa
