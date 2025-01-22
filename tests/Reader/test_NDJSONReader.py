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
