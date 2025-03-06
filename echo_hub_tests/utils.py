from collections.abc import Awaitable

Seconds = float


async def backoff[T](
    coro: Awaitable[T],
    *,
    retries: int = 3,
    sleep: Seconds = 1,
) -> T:
    assert retries > 0
    assert sleep >= 0.0
    last_err = None
    for _ in range(retries):
        try:
            return await coro
        except Exception as err:
            last_err = err
            print(f"retry {err=}")
    assert last_err is not None
    raise last_err
