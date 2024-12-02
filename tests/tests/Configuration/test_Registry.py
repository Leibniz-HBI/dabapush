"""Test suite for the Registry module."""

from importlib.metadata import EntryPoint

from dabapush.Configuration import Registry
from dabapush.Configuration.ReaderConfiguration import ReaderConfiguration
from dabapush.Configuration.WriterConfiguration import WriterConfiguration


def test_readers():
    """Should fetch readers from the reader entry point."""
    assert isinstance(Registry.readers(), list)
    assert all(isinstance(_, EntryPoint) for _ in Registry.readers())


def test_writers():
    """Should fetch writers from the writer entry point."""
    assert isinstance(Registry.writers(), list)
    assert all(isinstance(_, EntryPoint) for _ in Registry.writers())


def test_get_reader():
    """Should fetch a reader by name."""
    reader = Registry.get_reader("NDJSON")
    assert reader is not None
    assert issubclass(reader, ReaderConfiguration)


def test_get_writer():
    """Should fetch a writer by name."""
    writer = Registry.get_writer("NDJSON")
    assert writer is not None
    assert issubclass(writer, WriterConfiguration)


def test_list_all_readers():
    """Should list all available readers."""
    assert isinstance(Registry.list_all_readers(), list)
    assert all(isinstance(_, str) for _ in Registry.list_all_readers())


def test_list_all_writers():
    """Should list all available writers."""
    assert isinstance(Registry.list_all_readers(), list)
    assert all(isinstance(_, str) for _ in Registry.list_all_readers())
