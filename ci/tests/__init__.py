import logging
import string
from functools import reduce
from math import ceil, floor

from cuid2 import cuid


def id_to_b36(id: str) -> int:
    return reduce(lambda r, v: r * 36 + int(v, 36), [*id])


def is_base36(text: str) -> bool:
    alphabet: str = string.digits + string.ascii_lowercase
    return all(char in alphabet for char in text)


def build_histogram(numbers: list[int], bucket_count: int = 20) -> list[int]:
    buckets: list[int] = [0 for _ in range(0, bucket_count)]
    bucket_length: int = ceil(36 ** 23 / bucket_count)

    for number in numbers:
        bucket: int = floor(number / bucket_length)
        buckets[bucket] += 1

    return buckets


async def create_id_pool(max: int = 100000) -> tuple[list[int], list[int], list[int]]:
    id_pool_set: set[int] = set()

    for i in range(0, max):
        id_pool_set.add(cuid())
        logging.info(f'ID Pool Generation {floor((i/max) * 100)}% done')

        if len(id_pool_set) < i:
            logging.info(f'Collision detected at {i}')
            break

    id_pool: list[int] = list(id_pool_set)
    numbers: list[int] = list(map(lambda id: id_to_b36(str(id)[1:]), id_pool))
    histogram: list[int] = build_histogram(numbers)

    return (id_pool, numbers, histogram)
