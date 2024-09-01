"""Tests for aioh.limited_concurrency module."""
import asyncio
import time
import pytest
from aioh.limited_concurrency import with_limited_concurrency

@pytest.mark.asyncio
async def test_with_limited_concurrency_negative() -> None:
  """with_limited_concurrency should raise a ValueError."""
  with pytest.raises(ValueError):
    await asyncio.gather(*with_limited_concurrency(-1, []))

@pytest.mark.asyncio
async def test_with_limited_concurrency_zero() -> None:
  """with_limited_concurrency should raise a ValueError."""
  with pytest.raises(ValueError):
    await asyncio.gather(*with_limited_concurrency(0, []))

@pytest.mark.parametrize("concurrency", [1, 2, 3, 4, 5])
@pytest.mark.asyncio
async def test_with_limited_concurrency_x(concurrency: int) -> None:
  """with_limited_concurrency should work with x max concurrency."""
  async def task(n: int) -> int:
    return n * n

  tasks = [
    task(1),
    task(2),
    task(3),
    task(4),
  ]
  actual = await asyncio.gather(*with_limited_concurrency(concurrency, tasks))

  assert [1, 4, 9, 16] == actual

@pytest.mark.asyncio
async def test_with_limited_concurrency_lower_limit() -> None:
  """with_limited_concurrency should limit concurrency."""
  sleep_sec = 0.01
  async def task(n: int) -> int:
    await asyncio.sleep(sleep_sec)
    return n * n

  tasks = [
    task(1),
    task(2),
    task(3),
    task(4),
  ]
  start = time.time()
  actual = await asyncio.gather(*with_limited_concurrency(2, tasks))
  end = time.time()
  elapsed_sec = end - start

  tasks_no_limit = [
    task(1),
    task(2),
    task(3),
    task(4),
  ]
  start_no_limit = time.time()
  actual_no_limit = await asyncio.gather(*tasks_no_limit)
  end_no_limit = time.time()
  elapsed_sec_no_limit = end_no_limit - start_no_limit

  assert [1, 4, 9, 16] == actual
  assert actual_no_limit == actual
  # If concurrency is not limited, then it would finish everything all at once, meaning
  # elapsed_sec_no_limit should be only a little bit larger than 0.01 but not as large as 0.02.
  assert 0.01 < elapsed_sec_no_limit < 0.02
  # But with a concurrency limit of 2, it would mean at max there should be only 2 tasks running concurrently
  # at the same time. This should double the overall execution time.
  assert 0.02 < elapsed_sec

@pytest.mark.asyncio
async def test_with_limited_concurrency_higher_limit() -> None:
  """with_limited_concurrency should work when the max concurrency exceeds the length of coroutines."""
  async def task(n: int) -> int:
    return n * n

  tasks = [
    task(1),
    task(2),
    task(3),
    task(4),
  ]

  assert [1, 4, 9, 16] == await asyncio.gather(*with_limited_concurrency(5, tasks))
