import pytest
from pyutil.dicts import sort_dict


class Dicts:
    flat_dict = "flat_dict"
    nested_dict = "nested_dict"


@pytest.fixture
def input():
    return {
        Dicts.flat_dict: {
            "a": 1,
            "c": [1, 2, 3, 4],
            "d": "abc",
            "b": 2,
        },
        Dicts.nested_dict: {
            "a": 1,
            "c": {
                "b": 1,
                "a": 3,
            },
            "0": [1, 2, 3],
        },
    }


@pytest.fixture
def expected():
    return {
        Dicts.flat_dict: {
            "a": 1,
            "b": 2,
            "c": [1, 2, 3, 4],
            "d": "abc",
        },
        Dicts.nested_dict: {
            "0": [1, 2, 3],
            "a": 1,
            "c": {
                "a": 3,
                "b": 1,
            },
        },
    }


@pytest.mark.parametrize("dict_type", [Dicts.flat_dict, Dicts.nested_dict])
def test_sort_dict(input, expected, dict_type):
    input = input[dict_type]
    expected = expected[dict_type]
    assert sort_dict(input) == expected
