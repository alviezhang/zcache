import functools

from .backend import RedisBackend
from .zcache import ZCache

RedisCache = functools.partial(ZCache, RedisBackend)

__all__ = ["RedisCache", "ZCache"]
