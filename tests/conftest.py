"""Common fixtures for tests."""

import pytest


@pytest.fixture()
def isolated_test_dir(monkeypatch, tmp_path):
    """Create an isolated test tmp-directory."""
    monkeypatch.chdir(tmp_path)
    yield tmp_path
