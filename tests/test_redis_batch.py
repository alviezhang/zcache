import random

from zcache import RedisCache


def test_batch_function(redis_client):
    redis_client.flushall()
    cache = RedisCache(conn=redis_client)

    class A:
        def __init__(self):
            self.count = 0

        @cache.batch()
        def list(self, *ids):
            for _id in ids:
                self.count += 1
            return [2 * _id for _id in ids]

    a = A()
    assert a.list(1, 2, 3, 4, 5) == [2, 4, 6, 8, 10]
    assert a.count == 5
    assert a.list(1, 2) == [2, 4]
    assert a.count == 5
    assert a.list(5, 6, 7) == [10, 12, 14]
    assert a.count == 7
    assert a.list() == []
    assert a.count == 7
    a.list.invalidate(5, 7)
    assert a.list(1, 2, 5, 6, 7) == [2, 4, 10, 12, 14]
    assert a.count == 9


def test_batch_classmethod(redis_client):
    redis_client.flushall()
    cache = RedisCache(conn=redis_client)

    class AB:

        count = 0

        @cache.batch()
        @classmethod
        def list(cls, *ids):
            result = []
            for i in ids:
                result.append(i + random.randint(1, 100))
            return result

        @cache.batch()
        @classmethod
        def list2(cls, *ids):
            cls.__name__ = "ABC"
            result = []
            for i in ids:
                result.append(i + random.randint(1, 100))
            return result

    assert AB.list(3, 4) == AB.list(3, 4) == AB().list(3, 4)
    assert AB.list2(3, 4) != AB.list2(3, 4)


def test_batch_staticmethod(redis_client):
    redis_client.flushall()
    cache = RedisCache(conn=redis_client)

    class ABS:

        count = 0

        @cache.batch()
        @staticmethod
        def list(*ids):
            result = []
            for i in ids:
                result.append(i + random.randint(1, 100))
            return result

    assert ABS.list(3, 4) == ABS.list(3, 4) == ABS().list(3, 4)
