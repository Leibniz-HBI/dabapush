"Backlog for keeping track of already written records."

import dbm
from pathlib import Path
from shutil import copy
from typing import Any, Dict, List, Union

import ujson

from .Configuration.WriterConfiguration import WriterConfiguration
from .Record import Record


class BacklogLockedException(Exception):
    """Raised when trying to open a locked backlog"""

    def __init__(self):
        super().__init__("Can not open locked backlog.")


class UuidExistsException(Exception):
    """Raise when an entry exists in the db
    with the same uuid as the written record"""

    def __init__(self, uuid):
        super().__init__(f"Record with uuid {uuid} already exists in the db.")


class Backlog:
    """A backlog for keeping track of written Records."""

    def __init__(
        self,
        writer_config: WriterConfiguration,
    ):
        """Initialize the backlog configuration.

        Args:
            writer_config: The config used for the writer.
                This is mainly used for getting the name."""
        self.writer_config = writer_config
        self._db_connection = None
        self._locked = False

    def load(self):
        """Load the backlog from the file system."""
        dabapush_dir = Path(".dabapush")
        if not dabapush_dir.exists():
            dabapush_dir.mkdir()
        log_dir = self._backlog_root_dir
        if not log_dir.exists():
            log_dir.mkdir(parents=True)

        if self._log_lock_path.exists():
            raise BacklogLockedException()
        self._log_lock_path.touch()
        self._locked = True
        self._init_db()
        self._load_db()

        log_file_pth = dabapush_dir / f"{self.writer_config.name}.jsonl"
        if log_file_pth.exists():
            self._convert_log(log_file_pth)
            copy(log_file_pth, log_file_pth.with_suffix(log_file_pth.suffix + ".old"))
            log_file_pth.unlink()

    def _convert_log(self, log_file_pth):
        with open(log_file_pth, "rt", encoding="utf8") as log_file:
            for line in log_file.readlines():
                record_json = ujson.loads(line)  # pylint: disable=c-extension-no-member
                self._write_json_record(record_json)

    def _init_db(self):
        if not self._backlog_db_path.exists():
            _db = dbm.open(self._backlog_db_path.as_posix(), "c")
            _db.close()

    def write_record(self, record: Record):
        """Persist a record to the log"""
        if self._locked:
            log_dict = record.to_log()
            self._write_json_record(log_dict)

    @property
    def _log_lock_path(self) -> Path:
        return self._backlog_root_dir / "lock"

    @property
    def _backlog_db_path(self) -> Path:
        return self._backlog_root_dir / "backlog.db"

    @property
    def _backlog_root_dir(self) -> Path:
        return Path(f".dabapush/{self.writer_config.name}/backlog")

    def _write_json_record(
        self, record_dict: Dict[str, Union[str, List[Dict[str, Any]]]]
    ):
        uuid = record_dict["uuid"]
        if uuid in self._db_connection:
            raise UuidExistsException(uuid)
        self._db_connection[uuid] = ujson.dumps(
            record_dict
        )  # pylint: disable=c-extension-no-member

    def _load_db(self):
        if self._db_connection is None:
            self._db_connection = dbm.open(self._backlog_db_path.as_posix(), "w")

    def __contains__(self, item: Record):
        if not isinstance(item, Record):
            raise TypeError("Can only check for the the presence of records")
        uuid = item.uuid
        return uuid in self._db_connection

    def close(self):
        """Unlocks the log."""
        lock_pth = self._log_lock_path
        if lock_pth.exists():
            lock_pth.unlink()
        self._locked = False
        if self._db_connection is not None:
            self._db_connection.close()

    def __del__(self):
        self.close()
