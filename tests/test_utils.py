"""Test suite for the utils module."""

import pytest

from dabapush.utils import Timer, flatten, safe_access, safe_write, unpack

# pylint: disable=W0622


@pytest.mark.parametrize(
    "nested_dict, namespace, expected",
    [
        ({"a": {"b": "yuk"}}, None, {"a.b": "yuk"}),
        (
            {"a": {"b": "yuk", "c": [{"d": "meh"}]}},
            None,
            {"a.b": "yuk", "a.c": [{"d": "meh"}]},
        ),
        ({"a": {"b": "yuk"}}, "namespace", {"namespace.a.b": "yuk"}),
    ],
)
def test_flatten(nested_dict, namespace, expected):
    """Should flatten dicts correctly."""
    assert flatten(nested_dict, namespace=namespace) == expected


@pytest.mark.parametrize(
    "nested_dict, path, expected",
    [
        ({"a": {"b": {"c": "value"}}}, ["a", "b", "c"], "value"),
        ({"a": {"b": {"c": "value"}}}, ["a", "b", "d"], None),
        ({"a": {"b": {"c": "value"}}}, ["a", "b"], {"c": "value"}),
    ],
)
def test_safe_access(nested_dict, path, expected):
    """Should safely access nested dicts."""
    assert safe_access(nested_dict, path) == expected


@pytest.mark.parametrize(
    "nested_dict, path, key, value, expected",
    [
        (
            {"a": {"b": {"c": "value"}}},
            ["a", "b"],
            "d",
            "new_value",
            {"a": {"b": {"c": "value", "d": "new_value"}}},
        ),
        (
            {"a": {"b": {"c": "value"}}},
            ["a", "b", "e"],
            "f",
            "another_value",
            {"a": {"b": {"c": "value", "e": {"f": "another_value"}}}},
        ),
    ],
)
def test_safe_write(nested_dict, path, key, value, expected):
    """Should safely write to nested dicts."""
    assert safe_write(nested_dict, path, key, value) == expected


@pytest.mark.parametrize(
    "includes, id, id_key, expected",
    [
        (
            [{"id": "1", "name": "item1"}, {"id": "2", "name": "item2"}],
            "1",
            "id",
            {"id": "1", "name": "item1"},
        ),
        ([{"id": "1", "name": "item1"}, {"id": "2", "name": "item2"}], "3", "id", None),
    ],
)
def test_unpack(includes, id, id_key, expected):
    """Should unpack a dict from a list of dicts."""
    assert unpack(id, includes, id_key) == expected


@pytest.mark.parametrize("n", [10, 100, 1000])
def test_timer(n: int):
    """Test the timer utility."""

    t = Timer(micros=n)
    t.mark()

    while True:
        if not t.ok(auto_reset=False):
            assert t.elapsed_at_last_request <= n
        else:
            assert t.elapsed_at_last_request > n
            break
