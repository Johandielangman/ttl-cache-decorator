import time

import pytest

from ttl_cache import ttl_lru_cache


def test_cache_hit() -> None:
    calls = 0

    @ttl_lru_cache(ttl=2, jitter=1, maxsize=32)
    def cached_function(x: int) -> int:
        nonlocal calls
        calls += 1
        return x * 2

    # First call: miss
    assert cached_function(2) == 4
    assert calls == 1

    # Same argument within TTL: hit
    assert cached_function(2) == 4
    assert calls == 1

    # Different argument: miss
    assert cached_function(3) == 6
    assert calls == 2

    # Wait past one full TTL so the bucket is guaranteed to roll over
    time.sleep(2.1)

    # Same argument after expiry: miss again
    assert cached_function(2) == 4
    assert calls == 3

    info = cached_function.cache_info()
    assert (info.hits, info.misses) == (1, 3)


def test_negative_jitter():
    with pytest.raises(ValueError, match=r"jitter must be non-negative, got -1"):

        @ttl_lru_cache(ttl=2, jitter=-1, maxsize=32)
        def cached_function(x: int) -> int:
            return x * 2


def test_negative_ttl():
    with pytest.raises(ValueError, match=r"ttl must be positive, got -2"):

        @ttl_lru_cache(ttl=-2, jitter=1, maxsize=32)
        def cached_function(x: int) -> int:
            return x * 2
