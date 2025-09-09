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


def test_skips_progressed(isolated_test_dir: Path, data):  # pylint: disable=W0621
    """Should skip already progressed data."""
    reader = NDJSONReader(
        NDJSONReaderConfiguration("test", read_path=str(isolated_test_dir.resolve()))
    )
    file_path = isolated_test_dir / "test.ndjson"
    progress = -1
    with file_path.open("wt") as file:
        for idx, line in enumerate(data):
            json.dump(line, file)
            file.write("\n")
            if idx == 9:
                progress = file.tell()

    record_iter = reader.read()
    next(record_iter)  # init size
    reader.set_progress(file_path.as_posix(), progress)
    records = list(record_iter)
    assert len(records) == 10
    for n, record in enumerate(records):
        assert record.payload == data[n + 10]
