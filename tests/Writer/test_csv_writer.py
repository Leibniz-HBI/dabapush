"""Tests for CSVWriter class."""

import pytest

from dabapush.Record import Record
from dabapush.Writer.CSVWriter import CSVWriterConfiguration

# pylint: disable=W0621


@pytest.fixture
def config_factory():
    """Return a factory for CSVWriterConfiguration.

    Parameters
    ----------
    path : str
        The path to write to.

    Returns
    -------
    function
        A factory function that returns a CSVWriterConfiguration.
    """
    yield lambda path: CSVWriterConfiguration(
        name="test", chunk_size=1000000, path=str(path)
    )


@pytest.mark.parametrize(
    "data, expected",
    [
        ([{"key1": "value1"}, {"key2": "value2"}], "key1,key2\nvalue1,\n,value2\n"),
        ([{"key1": "value1", "key2": "value2"}], "key1,key2\nvalue1,value2\n"),
    ],
)
def test_write_csv(data, expected, config_factory, tmp_path):
    """Should write the correct data to the file."""
    config = config_factory(path=tmp_path)
    writer = config.get_instance()
    writer.write((Record(payload=d) for d in data))
    writer.persist()

    files = tmp_path.glob("*.csv")

    data = [file.read_text() for file in files]

    assert data[0] == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ([{"key1": "value1"}, {"key2": "value2"}], 3),  # 1 header + 2 data rows
        ([{"key1": "value1", "key2": "value2"}], 2),  # 1 header + 1 data row
    ],
)
def test_write_csv_line_count(data, expected, config_factory, tmp_path):
    """Should write the correct number of lines to the file."""
    config = config_factory(path=tmp_path)
    writer = config.get_instance()
    writer.write((Record(payload=d) for d in data))
    writer.persist()

    files = tmp_path.glob("*.csv")

    data = [file.read_text() for file in files]

    print(data)

    assert (len(data[0].split("\n")) - 1) == expected
