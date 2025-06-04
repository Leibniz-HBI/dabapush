"""NDJSON Writer plug-in for dabapush"""

from pathlib import Path

# pylint: disable=R,I1101
from typing import Iterator

import ujson
from loguru import logger as log

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record
from ..utils import Timer, flatten
from .Reader import StatefulFileReader


class NDJSONReader(StatefulFileReader):
    """Reader to read ready to read NDJSON data.
    It matches files in the path-tree against the pattern and reads all
    files and all lines in these files as JSON.

    Attributes
    ----------
    config: NDJSONRreaderConfiguration
        The configuration file used for reading
    """

    def __init__(self, config: "NDJSONReaderConfiguration") -> None:
        super().__init__(config)
        self.config = config
        self._timer = Timer(micros=10000)  # 10 ms timer for reading

    def read(self) -> Iterator[Record]:
        """reads multiple NDJSON files and emits them line by line"""

        for file_record in self.records:
            yield from file_record.split(
                func=self.read_and_split, flatten_records=self.config.flatten_dicts
            )

    def read_and_split(
        self,
        record: Record,
        flatten_records: bool = False,
    ) -> Iterator[Record]:
        """Reads a file and splits it into records by line."""
        path: Path = record.payload

        self._timer.mark()

        if not path:
            raise ValueError("Record payload must be a valid file path.")
        with path.open("rt", encoding="utf8") as file:
            # read the file line by line and create a Record for each line
            done = False
            stat = path.stat()
            offset = (
                self._state[str(record.uuid)] if str(record.uuid) in self._state else 0
            )
            if isinstance(offset, bytes):
                # if the offset is a byte string, decode it to a string
                offset = offset.decode("utf-8")
            if offset == "start":
                offset = 0
            offset = int(offset)
            # if the offset is larger than the file size, the file has been overwritten on disk,
            # and we need to start reading from the beginning.
            if offset >= stat.st_size:
                offset = 0
            file.seek(offset)
            # read the file line by line
            while not done:
                line = file.readline()
                position = file.tell()
                if not line and position >= stat.st_size:
                    done = True
                    continue
                payload = (
                    ujson.loads(line)
                    if not flatten_records
                    else flatten(ujson.loads(line))
                )
                child = Record(
                    uuid=f"{record.uuid}:{str(position)}",
                    payload=payload,
                    source=record,
                )
                record.children.append(child)

                yield child

                if self._timer.ok():
                    log.debug(
                        f"Setting state for {record.uuid} at position {position}."
                    )
                    self._state[str(record.uuid)] = str(position)


class NDJSONReaderConfiguration(ReaderConfiguration):
    """Read new line delimited JSON files.

    Attributes
    ----------
    flatten_dicts: bool
        whether to flatten those nested dicts

    """

    yaml_tag = "!dabapush:NDJSONReaderConfiguration"
    """internal tag for pyYAML
    """

    def __init__(
        self,
        name,
        id=None,  # pylint: disable=W0622
        read_path: str = ".",
        pattern: str = "*.ndjson",
        flatten_dicts=True,
    ) -> None:
        """
        Parameters
        ----------
        name: str
            target pipeline name
        id : UUID
            ID of the instance (default value = None, is set by super class)
        read_path: str
            path to directory to read
        pattern: str
            filename pattern to match files in `read_path` against
        flatten_dicts: bool
            whether nested dictionaries are flattened (for details see `dabapush.utils.flatten`)

        """
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)
        self.flatten_dicts = flatten_dicts

    def get_instance(self) -> NDJSONReader:  # pylint: disable=W0221
        """Get a configured instance of NDJSONReader

        Returns
        -------
        type: NDJSONReader
            Configured instance of NDJSONReader
        """
        return NDJSONReader(self)
