"""This module contains the abstract base class for all reader plugins."""

import abc
from dbm import gnu
from pathlib import Path
from typing import Iterator, List, Set

from loguru import logger as log
from tqdm.auto import tqdm

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record

# pylint: disable=I1101


class Reader(abc.ABC):
    """Abstract base class for all reader plugins.

    **BEWARE**: readers and writers are never to be instanced directly by the user but rather will
    be obtained by calling `get_instance()` on their specific Configuration-counterparts.

    Args:
        config (ReaderConfiguration): The configuration for the reader.
    """

    def __init__(self, config: ReaderConfiguration):
        """
        Parameters
        ----------
        config : ReaderConfiguration
            Configuration file for the reader. In concrete classes it will
            be a subclass of ReaderConfiguration.
        """
        self.config = config

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """

    @property
    @abc.abstractmethod
    def records(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """


class FileReader(Reader):
    """Reader to read files from a path.

    It matches files in the path-tree against the pattern.
    """

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Reads all files matching the pattern in the read_path."""

    @property
    def records(self) -> Iterator[Record]:
        """Generator for all files matching the pattern in the read_path."""
        ignored_files = self._get_ignored_files_()
        files = Path(self.config.read_path).rglob(self.config.pattern)
        # Filter out ignored files
        files = [f for f in files if f not in ignored_files]

        for a in tqdm(
            files,
            desc="Reading files",
        ):
            # Create a Record for each file found
            yield Record(
                uuid=str(a),
                payload=a,
            )

    def _get_ignored_files_(self) -> Set[Path]:
        # Collect all .dabapushignore files
        ignore_files: List[Path] = list(
            Path(self.config.read_path).rglob(".dabapushignore")
        )

        log.debug(f"Found {len(ignore_files)} ignore files in {self.config.read_path}")

        # Evaluate glob patterns in the ignore files
        files_to_ignore = []

        for ignore_file in ignore_files:
            with ignore_file.open("r", encoding="utf8") as f:

                log.debug(f"Reading ignore file: {ignore_file}")

                for line in f.readlines():
                    # Ignore empty lines and comments
                    if not line.strip() or line.startswith("#"):
                        continue
                    # Expand the glob pattern and add to the list
                    # Use Path.glob to ensure it works with relative paths
                    # from the ignore file's parent directory
                    log.debug(f"Processing line: {line.strip()} in {ignore_file}")
                    _files_ = Path(ignore_file.parent).glob(line.strip())
                    if _files_:
                        files_to_ignore.extend(list(_files_))
                    else:
                        continue

        # Deduplicate the list of files to ignore
        return set(files_to_ignore)


class StatefulFileReader(FileReader):
    """A file reader that maintains state across reads.

    This class extends FileReader to provide functionality for reading files
    while keeping track of the state of the reading process.
    """

    def __init__(self, config: ReaderConfiguration):
        super().__init__(config)
        self._state_path = Path(".dabapush") / config.name / "reader_state"
        if not self._state_path.parent.exists():
            self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state = gnu.open(self._state_path, "c")

    @property
    def records(self) -> Iterator[Record]:
        """Generator for all files matching the pattern in the read_path."""
        for record in super().records:
            # Check if the record has been processed before
            if record.uuid in self._state:
                log.debug(f"Already known record: {record.uuid}")
                # Determine whether the record was updated since last read

            # Mark the record as processed
            yield record

            self._state[record.uuid] = record.state
