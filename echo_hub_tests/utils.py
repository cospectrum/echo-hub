import asyncio
from collections.abc import Awaitable, Callable

Seconds = float


async def backoff[T](
    fn: Callable[[], Awaitable[T]],
    *,
    retries: int = 3,
    sleep: Seconds = 1,
) -> T:
    assert retries > 0
    assert sleep >= 0.0
    last_err = None
    for _ in range(retries):
        try:
            return await fn()
        except Exception as err:
            last_err = err
        await asyncio.sleep(sleep)
    assert last_err is not None
    raise last_err
