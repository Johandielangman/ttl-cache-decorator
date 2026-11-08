---
icon: lucide/timer
---

# TTL Cache

An LRU cache decorator with a ==time to live==. `ttl_lru_cache` works exactly
like [`functools.lru_cache`][lru_cache], except entries automatically expire
after a configurable number of seconds.

  [lru_cache]: https://docs.python.org/3/library/functools.html#functools.lru_cache

## Installation

=== "pip"

    ``` console
    pip install ttl-cache-decorator
    ```

=== "uv"

    ``` console
    uv add ttl-cache-decorator
    ```

Requires **Python 3.12+**.

## Quickstart

``` python title="Basic usage" hl_lines="1 4"
from ttl_cache import ttl_lru_cache


@ttl_lru_cache(ttl=30)  # (1)!
def fetch_user(user_id: int) -> dict:
    print("Fetching from the network...")
    return {"id": user_id, "name": "Ada"}


fetch_user(1)  # Prints "Fetching from the network..."
fetch_user(1)  # Cache hit, nothing printed
# ... 30 seconds later ...
fetch_user(1)  # Expired — fetches again
```

1.  Cache results for 30 seconds. While the TTL window is open, repeat calls
    with the same arguments are served from the cache.

## How it works

Under the hood it still uses `lru_cache`, but the cached call receives an extra
positional-only *time bucket* argument derived from a monotonic clock:

``` python title="The time bucket"
time_bucket = int((time.monotonic() + offset) // ttl)
```

An entry stays "alive" while the bucket value is unchanged and expires when the
bucket rolls over:

``` mermaid
graph LR
  A[Call] --> B{Bucket changed?}
  B -->|No| C[Serve cached value]
  B -->|Yes| D[Recompute and cache]
  C --> E[Return]
  D --> E
```

!!! note

    The bucket boundary is shared per TTL window, so an entry lives for *at
    most* `ttl` seconds and *at least* the remainder of the current bucket.

## API reference

### `ttl_lru_cache`

``` python
ttl_lru_cache(
    ttl: float = 60,
    jitter: float = 0,
    maxsize: int | None = 128,
    typed: bool = False,
)
```

| Parameter | Type | Default | Description |
|---|---|---|---|
| `ttl` | `float` | `60` | Time to live in seconds. Must be positive. |
| `jitter` | `float` | `0` | Max random offset (seconds) applied to bucket boundaries. Must be non-negative. |
| `maxsize` | `int \| None` | `128` | Max size of the cache, or `None` for unbounded. |
| `typed` | `bool` | `False` | Whether argument types are part of the cache key. |

Returns a decorator whose wrapped function keeps its signature and exposes the
usual `lru_cache` helpers: `cache_info()` and `cache_clear()`.

!!! warning "Validation"

    A `ValueError` is raised at decoration time if `ttl` is not positive or
    `jitter` is negative.

### Jitter

`jitter` draws a random offset once per decorated function from
`random.uniform(0, jitter)`, so different functions (or processes) expire at
different moments instead of all at once. Use it to avoid a *thundering herd*
when many cached values would otherwise expire simultaneously:

``` python title="Adding jitter" hl_lines="1"
@ttl_lru_cache(ttl=60, jitter=10)
def fetch_metrics(service: str) -> dict: ...
```

### Cache helpers

``` python title="Inspecting and clearing the cache"
fetch_user.cache_info()  # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)
fetch_user.cache_clear()  # Drop all cached entries
```

??? info "Typing"

    The decorator is fully generic via `ParamSpec` and returns a
    `TTLCachedFunction` protocol, so type checkers preserve the wrapped
    function's signature — including keyword arguments.

    ``` python
    from ttl_cache import TTLCachedFunction

    cached_fetch: TTLCachedFunction[[str], dict] = ttl_lru_cache(ttl=5)(fetch_user)
    ```

## License

`ttl-cache-decorator` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
