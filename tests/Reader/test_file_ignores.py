"""Test for the ignores file functionality in FileReader.

.dabapushignore file(s) should be respected by the FileReader.
"""

from pathlib import Path
from typing import Iterator

from dabapush.Configuration.ReaderConfiguration import ReaderConfiguration
from dabapush.Reader.Reader import FileReader
from dabapush.Record import Record


class TestReader(FileReader):
    """Test Reader for testing the ignores file functionality."""

    def read(self) -> Iterator[Record]:
        pass


def test_ignores_file(isolated_test_dir):
    """Test that the ignores file is correctly loaded."""
    file_to_ignore = "ignored.txt"

    reader = TestReader(
        ReaderConfiguration(
            name="test",
            id="test_id",
            read_path=str(isolated_test_dir.resolve()),
            pattern="*.txt",
        )
    )

    # Create an ignored file
    ignore_file = isolated_test_dir / ".dabapushignore"
    ignore_file.write_text(f"{file_to_ignore}\n", encoding="utf8")

    # Create a file that should be ignored
    ignored_file_path = isolated_test_dir / file_to_ignore
    ignored_file_path.write_text("This file should be ignored.")

    # Ensure the file is in the ignored files set
    assert (
        Path(file_to_ignore).resolve()
        in reader._get_ignored_files_()  # pylint: disable=protected-access
    )
