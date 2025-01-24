"Backlog for keeping track of already written records."
from pathlib import Path
from shutil import copy
from sqlite3 import IntegrityError, connect
from typing import Any, Dict, List, Union

import ujson

from .Configuration.WriterConfiguration import WriterConfiguration
from .Record import Record

_backlog_table_name = "dabapush_backlog"


class BacklogLockedException(Exception):
    "Raised when trying to open a locked backlog"

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
        self._sqlite_connection = None
        self._locked = False

    def load(self):
        "Load the backlog from the file system."
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
        log_file_pth = dabapush_dir / f"{self.writer_config.name}.jsonl"
        if log_file_pth.exists():
            self._convert_log(log_file_pth)
            copy(log_file_pth, log_file_pth.with_suffix(log_file_pth.suffix + ".old"))
            log_file_pth.unlink()
        self._load_db()

    def _convert_log(self, log_file_pth):
        self._init_db()
        with open(log_file_pth, "rt", encoding="utf8") as log_file:
            for line in log_file.readlines():
                record_json = ujson.loads(line)  # pylint: disable=c-extension-no-member
                self._write_json_record(record_json)

    def _init_db(self):
        if self._sqlite_connection is None:
            self._sqlite_connection = connect(self._backlog_db_path.as_posix())
        columns = self._sqlite_connection.execute(
            f"""SELECT name
            FROM sqlite_schema
            WHERE name='{_backlog_table_name}'"""
        )
        column = columns.fetchone()
        if column is None:
            self._sqlite_connection.execute(
                f"""CREATE TABLE {_backlog_table_name}(uuid TEXT PRIMARY KEY, record)"""
            )

    def write_record(self, record: Record):
        "Persist a record to the log"
        if self._locked:
            log_dict = record.to_log()
            self._write_json_record(log_dict)

    @property
    def _log_lock_path(self) -> Path:
        return self._backlog_root_dir / "lock"

    @property
    def _backlog_db_path(self) -> Path:
        return self._backlog_root_dir / "backlog.sqlite3"

    @property
    def _backlog_root_dir(self) -> Path:
        return Path(f".dabapush/{self.writer_config.name}/backlog")

    def _write_json_record(
        self, record_dict: Dict[str, Union[str, List[Dict[str, Any]]]]
    ):
        uuid = record_dict["uuid"]
        try:
            self._sqlite_connection.execute(
                f"""INSERT INTO {_backlog_table_name} VALUES
                    (:uuid, :record)""",
                {
                    "uuid": uuid,
                    "record": ujson.dumps(  # pylint: disable=c-extension-no-member
                        record_dict
                    ),
                },
            )
            self._sqlite_connection.commit()
        except IntegrityError as exc:
            raise UuidExistsException(uuid) from exc

    def _load_db(self):
        if self._sqlite_connection is None:
            self._sqlite_connection = connect(self._backlog_db_path.as_posix())

    def __contains__(self, item: Record):
        if not isinstance(item, Record):
            raise TypeError("Can only check for the the presence of records")
        uuid = item.uuid
        results = self._sqlite_connection.execute(
            f"""SELECT uuid
            from {_backlog_table_name}
            where uuid='{uuid}'"""
        )
        return results.fetchone() is not None

    def close(self):
        "Unlocks the log."
        lock_pth = self._log_lock_path
        if lock_pth.exists():
            lock_pth.unlink()
        self._locked = False
        if self._sqlite_connection is not None:
            self._sqlite_connection.close()

    def __del__(self):
        self.close()
