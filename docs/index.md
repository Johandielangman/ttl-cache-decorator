---
icon: lucide/timer
---

# TTL Cache

[![PyPI - Version](https://img.shields.io/pypi/v/ttl-cache-decorator.svg)](https://pypi.org/project/ttl-cache-decorator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ttl-cache-decorator.svg)](https://pypi.org/project/ttl-cache-decorator)
[![CI](https://github.com/Johandielangman/ttl-cache-decorator/actions/workflows/ci.yml/badge.svg)](https://github.com/Johandielangman/ttl-cache-decorator/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Johandielangman/ttl-cache-decorator/graph/badge.svg)](https://codecov.io/gh/Johandielangman/ttl-cache-decorator)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://johandielangman.github.io/ttl-cache-decorator/)

An LRU cache decorator with a **time to live**. `ttl_lru_cache` works exactly
like [`functools.lru_cache`](https://docs.python.org/3/library/functools.html#functools.lru_cache), except entries automatically expire after a configurable number of seconds.

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
