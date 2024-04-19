"""Tests for the Record module.
"""
from pathlib import Path

from dabapush.Record import Record


def test_init():
    """Should initialize a Record."""
    record = Record({"key": "value"}, Path())
    assert record.uuid
    assert record.processed_at
    assert record.payload == {"key": "value"}
    assert record.source == Path()


def test_init_without_payload():
    """Should initialize a Record without a payload."""
    record = Record({}, Path())
    assert record.uuid
    assert record.processed_at
    assert not record.payload
    assert record.source == Path()


def test_splitting_record():
    """Should split a Record."""
    payload = {
        "key": [
            {"key": "value"},
            {"key": "value"},
            {"key": "value"},
        ]
    }

    record = Record(payload, Path())
    records = record.split("key")
    assert len(records) == 3
    for _record_ in records:
        assert _record_.uuid
        assert _record_.processed_at
        assert _record_.payload == {"key": "value"}
        assert _record_.source == Path()
        assert _record_ in record.children


def test_splitting_record_with_children_ids():
    """Should split a Record."""
    payload = {
        "key": [
            {"key": "value", "id": 1},
            {"key": "value", "id": 2},
            {"key": "value", "id": 3},
        ]
    }

    record = Record(payload, Path())
    records = record.split("key", id_key="id")
    assert len(records) == 3
    for n, _record_ in enumerate(records, 1):
        assert _record_.uuid == n
        assert _record_.processed_at
        assert _record_.payload == {"key": "value", "id": n}
        assert _record_.source is None
        assert _record_ in record.children


def test_splitting_record_without_key():
    """Should not split a Record without a key."""
    payload = {
        "key": [
            {"key": "value"},
            {"key": "value"},
            {"key": "value"},
        ]
    }

    record = Record(payload, Path())
    records = record.split("key2")
    assert len(records) == 0


def test_splitting_record_without_payload():
    """Should not split a Record without a payload."""
    record = Record({}, Path())
    records = record.split("key")
    assert len(records) == 0


def test_logging_record():
    """Should log a Record."""
    record = Record({"key": "value"}, Path())

    assert record.to_log() == {
        "source": str(Path()),
        "uuid": record.uuid,
        "processed_at": record.processed_at.isoformat(),
        "children": [],
    }
