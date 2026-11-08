# TTL Cache

[![PyPI - Version](https://img.shields.io/pypi/v/ttl-cache-decorator.svg)](https://pypi.org/project/ttl-cache-decorator)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ttl-cache-decorator.svg)](https://pypi.org/project/ttl-cache-decorator)
[![CI](https://github.com/Johandielangman/ttl-cache-decorator/actions/workflows/ci.yml/badge.svg)](https://github.com/Johandielangman/ttl-cache-decorator/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Johandielangman/ttl-cache-decorator/graph/badge.svg)](https://codecov.io/gh/Johandielangman/ttl-cache-decorator)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://johandielangman.github.io/ttl-cache-decorator/)

An LRU cache decorator with a time to live like `functools.lru_cache`, but entries expire after a configurable number of seconds.

## Installation

```console
pip install ttl-cache-decorator
```

## Usage

```python
from ttl_cache import ttl_lru_cache


@ttl_lru_cache(ttl=30)
def fetch_user(user_id: int) -> dict:
    return {"id": user_id, "name": "Ada"}


fetch_user(1)  # Calls the function
fetch_user(1)  # Cache hit
# ... 30 seconds later ...
fetch_user(1)  # Expired — calls the function again
```

## License

`ttl-cache-decorator` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
