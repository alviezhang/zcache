#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
from .backend import RedisBackend
from .zcache import Zcache

RedisCache = functools.partial(Zcache, RedisBackend)

__all__ = ['RedisCache']
