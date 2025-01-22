"""Test suite for package-level items."""

from dabapush import __version__


def test_version():
    """Should be the current version number."""
    assert __version__ == "0.4.0-alpha10"


def test_version_type():
    """Should be a string."""
    assert isinstance(__version__, str)
