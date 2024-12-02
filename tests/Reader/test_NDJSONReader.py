"""Tests for NDJSONReader."""

import json
from pathlib import Path

import pytest

from dabapush.Reader.NDJSONReader import NDJSONReader, NDJSONReaderConfiguration


@pytest.fixture
def data():
    """Returns a list of 20 dictionaries."""
    return [{"key": "value"} for _ in range(20)]


def test_read(isolated_test_dir: Path, data):  # pylint: disable=W0621
    """Should read the data from the file."""
    reader = NDJSONReader(
        NDJSONReaderConfiguration("test", read_path=str(isolated_test_dir.resolve()))
    )
    file_path = isolated_test_dir / "test.ndjson"
    with file_path.open("wt") as file:
        for line in data:
            json.dump(line, file)
            file.write("\n")

    records = list(reader.read())
    assert len(records) == 20
    for n, record in enumerate(records):
        assert record.processed_at
        assert record.payload == data[n]


def test_read_with_backlog(isolated_test_dir: Path, data):  # pylint: disable=W0621
    """Should only read the new data."""
    reader = NDJSONReaderConfiguration(
        "test", read_path=str(isolated_test_dir.resolve()), pattern="*.ndjson"
    ).get_instance()
    file_path = isolated_test_dir / "test.ndjson"
    with file_path.open("wt") as file:
        for line in data:
            json.dump(line, file)
            file.write("\n")

    def wrapper():
        n = None
        for n, record in enumerate(reader.read()):
            record.done()
        return n or 0

    n = wrapper()

    assert n + 1 == 20

    reader2 = NDJSONReaderConfiguration(
        "test", read_path=str(isolated_test_dir.resolve())
    ).get_instance()

    records2 = list(reader2.read())
    log_path = isolated_test_dir / ".dabapush/test.jsonl"
    assert log_path.exists()
    assert len(reader2.back_log) == 20
    assert len(records2) == 0
