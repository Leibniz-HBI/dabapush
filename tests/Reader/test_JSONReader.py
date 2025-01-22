"""Tests for NDJSONReader."""

import json
from pathlib import Path

import pytest

from dabapush.Reader.JSONReader import JSONReader, JSONReaderConfiguration


@pytest.fixture
def input_json_directory(isolated_test_dir):
    "Pytest fixture creating a directory with 20 json files."
    for idx in range(10, 30):
        file_path = isolated_test_dir / f"test_{idx}.json"
        with file_path.open("wt") as out_file:
            json.dump({"test_key": idx}, out_file)
            out_file.write("\n")
    return isolated_test_dir


def test_read(input_json_directory: Path):  # pylint: disable=W0621
    """Should read the data from the file."""
    reader = JSONReader(
        JSONReaderConfiguration("test", read_path=str(input_json_directory.resolve()))
    )
    records = list(reader.read())
    assert len(records) == 20
    for record in records:
        print(record)
        assert record.processed_at
        assert record.payload == {"test_key": int(record.uuid[-7:-5])}
