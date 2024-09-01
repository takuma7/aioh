"""Limited concurrency."""

import asyncio
from typing import Awaitable, Sequence, TypeVar


T = TypeVar("T")

def with_limited_concurrency(max_concurrency: int, coroutines: Sequence[Awaitable[T]]) -> list[Awaitable[T]]:
  """Return a list of awaitables with a limited concurrency.

  Args:
      max_concurrency (int): Maximum concurrency. Must be >= 1.
      coroutines (Sequence[Awaitable[T]]): A list of awaitable tasks to execute concurrently

  Returns:
      list[Awaitable[T]]: A list of async tasks with a limited concurrency. This can be passed to a bulk await e.g. asyncio.gather
  """
  if max_concurrency < 1:
    raise ValueError("max_concurrency must be >= 1")


  semaphore = asyncio.Semaphore(max_concurrency)

  async def run_with_limit(coroutine: Awaitable[T]) -> T:
    async with semaphore:
      return await coroutine
  
  return [run_with_limit(co) for co in coroutines]
