"""Test suite for the NDJSONWriter module."""

import pytest

from dabapush.Record import Record
from dabapush.Writer.NDJSONWriter import NDJSONWriterConfiguration


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            [{"key1": "value1"}, {"key2": "value2"}],
            '{"key1":"value1"}\n{"key2":"value2"}\n',
        ),
        ([{"key1": "value1", "key2": "value2"}], '{"key1":"value1","key2":"value2"}\n'),
    ],
)
def test_write_ndjson(data, expected, tmp_path):
    """Should write records to a file in NDJSON format."""
    configuration = NDJSONWriterConfiguration(
        name="test",
        id="test",
        chunk_size=1,
        path=str(tmp_path),
        name_template="test.ndjson",
    )
    file_path = tmp_path / "test.ndjson"
    writer = configuration.get_instance()
    writer.write((Record(_) for _ in data))

    with file_path.open("rt", encoding="utf8") as f:
        result = f.read()

    assert result == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([{"key1": "value1"}, {"key2": "value2"}], 2),
        ([{"key1": "value1", "key2": "value2"}], 1),
    ],
)
def test_write_ndjson_line_count(data, expected, tmp_path):
    """Should write records to a file in NDJSON format."""
    configuration = NDJSONWriterConfiguration(
        name="test",
        id="test",
        chunk_size=1,
        path=str(tmp_path),
        name_template="test.ndjson",
    )
    file_path = tmp_path / "test.ndjson"
    writer = configuration.get_instance()
    writer.write((Record(_) for _ in data))

    with file_path.open("rt", encoding="utf8") as f:
        result = f.readlines()

    assert len(result) == expected
