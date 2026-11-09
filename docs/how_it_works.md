---
icon: lucide/message-circle-question-mark
---

# How it works

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
