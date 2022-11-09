"""Test suite for dabapush.Configuration.FileWriterConfiguration"""
# pylint: disable=W0621
from pytest import fixture

from dabapush.Configuration.FileWriterConfiguration import FileWriterConfiguration


@fixture
def writer_config() -> FileWriterConfiguration:
    """Provides a FileWriterConfiguration for testing."""
    return FileWriterConfiguration("test")


def test_make_file_name(writer_config: FileWriterConfiguration):
    """Should create a file_name from a template."""
    writer_config.set_name_template("$name")
    name = writer_config.make_file_name()
    assert name == writer_config.name
