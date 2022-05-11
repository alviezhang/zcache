# ZCache

<!-- [![Pypi Status](https://img.shields.io/pypi/v/zcache.svg)](https://pypi.python.org/pypi/zcache) -->

> This project is a community version of [Tache](https://github.com/zhihu/tache).

## **THIS PROJECT IS STILL WIP, PLEASE DON'T USE**

ZCache is a caching framework for Python. It is designed with the following goals in mind:

* Support for Python 3.7+
* Support for caching common functions/instance methods/class methods/static methods
* Support for Batch Batch Caching
* Support for Tag-based caching and invalidation
* Support for explicitly declaring key formats based on parameters

[Github Repo](https://github.com/alviezhang/zcache)

## Features

* Cache null by default to prevent penetration
* Tag-based batch cache invalidation
* Batch caching
* Support `YAML`, `JSON`, `PICKLE` multiple backend serializer

## Documention

* [Tag Usage](docs/advance_tag.md)
* [Using keyword arguments](docs/use_kwargs.md)
* [Cache null values and cache penetration](docs/cache_null_and_miss.md)

## Getting Started

### Basic usage

```python
import random
import fakeredis
from zcache import RedisCache

redis_client = fakeredis.FakeStrictRedis()
cache = RedisCache(conn=redis_client, format="JSON")

@cache.cached()
def add(a, b):
    return a + b + random.randint(1,100)

result1 = add(5, 6)
# Cache value is not changed
assert add(5, 6) == result1
# Invalidate cached value
add.invalidate(5, 6)
assert add(5, 6) != result1
```

### Tag-based batch cache invalidation

The tag can be fixed or dynamic, where the dynamic parameter represents the position
of the argument in the function.

When a tag is invalidated, it means that all cache with the same tag under this function
are all invalidated.

```python
@cache.cached(tags=["a:{0}"])
def add(a, b):
    return a + b + random.randint(1,100)

result1 = add(5, 6)
result2 = add(5, 7)
add.invalidate_tag("a:5")
assert result1 != add(5, 6)
assert result2 != add(5, 7)
```

### Refresh cache

When `refresh` is called, the cache is refreshed and the latest value is returned.

```python
class A(object):

    def __init__(self):
        self.extra = 0

    @cache.cached()
    def add(self, a, b):
        self.extra += 1
        return a + b + self.extra

a = A()
assert a.add(5, 6) == 12
assert a.extra == 1
assert a.add.refresh(5, 6) == 13
assert a.extra == 2
```

### Batch cache mode

```python
@cache.batch()
def get_comments(*comment_ids):
    return [get_comment(c) for c in comment_ids]

get_comments(1,2,3,4,5) # no cache
get_comments(2,3,4,5,6) # get 2,3,4,5 from cache, call 6 first then cache
get_comments.invalidate(3,4,5) # invalidate 3,4,5
```

### Explicitly Specify Keys

ZCache allows you to explicitly specify rules for cache keys, so that the generated keys will remain unchanged regardless of code refactoring.

```python
class B:

    def __init__(self):
        self.count = 0

    @cache.cached("counter.B.add|{0}-{1}")
    def add(self, a, b):
        self.count += 1
        return a + b + self.count
```

### Note

We support `classmethod/staticmethod` keywords, but you must put `classmethod` inner when use it.

```python
class AC(object):

    @cache.cached()
    @classmethod
    def add(cls, a, b):
        return a + b + random.randint(1,100)
```

We also support namespaces. The default rule for key generation is `namespace:module.classname.func|arg1-arg2|tag1-tag2`, where `namespace` is empty, and `classname` is also empty if it does not exist.

```python
class A(object):
    @cache.cache(namespace="v1")
    def add(self, a, b):
        return db.execute(sql).fetchone()
```

In this example, if the database fields change, the namespace can be modified in such a way that the old and new code use different cached results.
