import os
import shutil

import pytest
from pyutil.cache import cached

TMP_CACHE_PATH = "tmp/cache"


def items_in_cache():
    return len(os.listdir(TMP_CACHE_PATH))


def empty_cache():
    shutil.rmtree(TMP_CACHE_PATH)


@pytest.fixture(autouse=True)
def cleanup():
    yield
    empty_cache()


class Parent:
    @cached(TMP_CACHE_PATH, is_method=True, instance_identifiers=["name"])
    def parent_fn(self, a, b, c, d=2, f={"b": 1, "a": 2}):
        return a + b + c + d


class Child_A(Parent):
    def __init__(self, name):
        self.name = name


class Child_B(Parent):
    def __init__(self, name):
        self.name = name


def test_is_method():
    a = Child_A("a")
    b = Child_B("b")

    a.parent_fn(1, 2, 3)
    assert items_in_cache() == 1

    b.parent_fn(1, 2, 3)
    assert items_in_cache() == 2

    empty_cache()

    a = Child_A("a")
    b = Child_B("a")

    a.parent_fn(1, 2, 3)
    assert items_in_cache() == 1

    b.parent_fn(1, 2, 3)
    assert items_in_cache() == 1


def test_identifiers():
    @cached(TMP_CACHE_PATH, identifiers=[1, 2, 3])
    def dummy_fn(a, b):
        return a + b

    @cached(TMP_CACHE_PATH, identifiers=[3, 2, 3])
    def dummy_fn_2(a, b):
        return a + b

    @cached(TMP_CACHE_PATH, identifiers=[1, 2, 3])
    def dummy_fn_3(a, b):
        return a + b

    dummy_fn(1, 2)
    dummy_fn_2(1, 2)
    assert items_in_cache() == 2
    dummy_fn_3(1, 2)
    assert items_in_cache() == 2


def test_logs():
    @cached(TMP_CACHE_PATH, log_level="INFO", identifiers=[4, 5])
    def dummy_fn(a, b):
        return a + b

    dummy_fn(1, 2)
    dummy_fn(1, 2)
