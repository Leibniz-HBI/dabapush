"""Test suite for package-level items."""

from dabapush import __version__


def test_version():
    """Should be the current version number."""
    assert __version__ == "0.3.3"
