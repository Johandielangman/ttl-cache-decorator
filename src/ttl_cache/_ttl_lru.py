import functools
import random
import time
from collections.abc import Callable
from functools import lru_cache, wraps
from typing import Any, Protocol, cast


class TTLCachedFunction[**P, R](Protocol):
    """Same signature as the wrapped function, plus ``lru_cache``'s helpers."""

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    def cache_info(self) -> functools._CacheInfo: ...
    def cache_clear(self) -> None: ...


def ttl_lru_cache[**P, R](
    ttl: float = 60,
    jitter: float = 0,
    maxsize: int | None = 128,
    typed: bool = False,
) -> Callable[[Callable[P, R]], TTLCachedFunction[P, R]]:
    """A decorator that works like ``lru_cache`` but with a time to live (ttl).

    Under the hood it still uses ``lru_cache``, but the cached call receives an
    extra positional-only ``time_bucket`` argument:

        time_bucket = int((time.monotonic() + offset) // ttl)

    An entry stays "alive" while the bucket value is unchanged and expires when
    the bucket rolls over. ``offset`` is drawn once per decorated function from
    ``random.uniform(0, jitter)``, so different functions (or processes) expire
    at different moments instead of all at once.

    Args:
        ttl: Time to live in seconds. Defaults to 60.
        jitter: Max random offset in seconds applied to the bucket boundaries.
            Defaults to 0.
        maxsize: Max size of the cache, or ``None`` for unbounded. Defaults to 128.
        typed: Whether argument types are part of the cache key. Defaults to False.

    Returns:
        A decorator that wraps a function in a TTL-aware LRU cache. The wrapped
        function keeps its signature and exposes ``cache_info`` and
        ``cache_clear``.

    Raises:
        ValueError: If ``ttl`` is not positive or ``jitter`` is negative.

    Example:

        >>> @ttl_lru_cache(ttl=30, jitter=5)
        ... def fetch(key: str) -> str:
        ...     return key.upper()
    """
    if ttl <= 0:
        raise ValueError(f"ttl must be positive, got {ttl!r}")
    if jitter < 0:
        raise ValueError(f"jitter must be non-negative, got {jitter!r}")

    def decorator(func: Callable[P, R]) -> TTLCachedFunction[P, R]:
        offset = random.uniform(0, jitter)

        @lru_cache(maxsize=maxsize, typed=typed)
        def cached_with_time(_time_bucket: int, /, *args: Any, **kwargs: Any) -> R:
            return func(*args, **kwargs)

        # lru_cache types its arguments as Hashable, which P.args/P.kwargs can't
        # be proven to be. Unhashable arguments still raise TypeError at call
        # time, exactly as with plain lru_cache.
        call_cached = cast(Callable[..., R], cached_with_time)

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            time_bucket = int((time.monotonic() + offset) // ttl)
            return call_cached(time_bucket, *args, **kwargs)

        wrapper.__dict__.update(
            cache_info=cached_with_time.cache_info,
            cache_clear=cached_with_time.cache_clear,
        )
        return cast(TTLCachedFunction[P, R], wrapper)

    return decorator
