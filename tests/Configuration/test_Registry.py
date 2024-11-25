"""Tests for dabapush.Configuration.Registry."""
from importlib.metadata import EntryPoint

from dabapush.Configuration import Registry


def test_readers():
    """Should fetch and instantiate readers from entry point."""
    readers = Registry.readers()

    assert isinstance(readers, tuple)
    assert all(isinstance(_, EntryPoint) for _ in readers)


def test_writers():
    """Should fetch and instantiate writers from entry point."""
    writers = Registry.writers()

    assert isinstance(writers, tuple)
    assert all(isinstance(_, EntryPoint) for _ in writers)
