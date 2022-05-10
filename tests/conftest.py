from __future__ import annotations

import os

from pytest import fixture
from redis import StrictRedis


@fixture
def redis_conf():
    return {
        "host": os.getenv("REDIS_HOST", "127.0.0.1"),
        "port": int(os.getenv("REDIS_PORT", "6379")),
    }


@fixture
def redis_client(redis_conf):
    return StrictRedis(**redis_conf)
