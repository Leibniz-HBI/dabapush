from collections import defaultdict
from hashlib import md5
from typing import Any, Dict, List, Union
from itertools import accumulate, islice
from pathlib import Path
from ujson import loads, dump

from .Configuration.WriterConfiguration import WriterConfiguration
from .Record import Record

_HEX_CHARS = "0123456789abcdef"


class BacklogLockedException(Exception):
    "Raised when trying to open a locked backlog"
    def __init__(self):
        super().__init__("Can not open locked backlog.")


class Backlog:
    """A backlog for keeping track of written Records."""

    def __init__(
        self,
        len_prefix_persist: int,
        len_prefix_memory: int,
        writer_config: WriterConfiguration,
    ):
        """Initialize the backlog configuration.

        Args:
            len_prefix_persist: Number of digits used for partitioning the log.
                Will result in 16 ** len_prefix_persist files on disk.
            len_prefix_memory: Number of digits used for partitioning the in memory log.
            writer_config: The config used for the writer.
                This is mainly used for getting the name."""
        self.len_prefix_persist = len_prefix_persist
        self.len_prefix_memory = len_prefix_memory
        self.writer_config = writer_config
        self.parts = defaultdict(set)
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
        self._init_dirs()
        log_file_pth = dabapush_dir / f"{self.writer_config.name}.jsonl"
        if log_file_pth.exists():
            self._convert_log(log_file_pth)
            log_file_pth.unlink()
        self._load_dir()

    def _convert_log(self, log_file_pth):
        self._init_dirs()
        with open(log_file_pth, "rt", encoding="utf8") as log_file:
            for line in log_file.readlines():
                record_json = loads(line)
                self._write_json_record(record_json)

    def _init_dirs(self):
        log_dir = self._backlog_root_dir
        file_prefixes = next(
            islice(
                accumulate(
                    [_HEX_CHARS] * self.len_prefix_persist,
                    lambda chars0, chars1: [
                        char0 + char1 for char0 in chars0 for char1 in chars1
                    ],
                ),
                self.len_prefix_persist - 1,
                self.len_prefix_persist,
            )
        )
        for prefix in file_prefixes:
            file_pth = log_dir / (prefix + ".jsonl")
            if not file_pth.exists():
                file_pth.touch()

    def write_record(self, record: Record):
        "Persist a record to the log"
        if self._locked:
            log_dict = record.to_log()
            self._write_json_record(log_dict)
            self._store_in_memory(log_dict)

    @property
    def _log_lock_path(self) -> Path:
        return self._backlog_root_dir / "lock"

    @property
    def _backlog_root_dir(self) -> Path:
        return Path(f".dabapush/{self.writer_config.name}/backlog")

    def _write_json_record(
        self, record_dict: Dict[str, Union[str, List[Dict[str, Any]]]]
    ):
        uuid = record_dict["uuid"]
        persist_prefix = md5(uuid.encode()).hexdigest()[: self.len_prefix_persist]
        with (self._backlog_root_dir / f"{persist_prefix}.jsonl").open(
            "+wt", encoding="utf8"
        ) as out_file:
            dump(record_dict, out_file)
            out_file.write("\n")

    def _load_dir(self):
        log_dir = self._backlog_root_dir
        for chunk_pth in log_dir.glob("*.jsonl"):
            with chunk_pth.open("rt", encoding="utf8") as chunk_file:
                for line in chunk_file.readlines():
                    record_dict = loads(line)
                    uuid = record_dict["uuid"]
                    memory_prefix = md5(uuid.encode()).hexdigest()[
                        : self.len_prefix_memory
                    ]
                    self.parts[memory_prefix].add(uuid)

    def __contains__(self, item: Record):
        if not isinstance(item, Record):
            raise TypeError("Can only check for the the presence of records")
        uuid = item.uuid
        memory_prefix = md5(uuid.encode()).hexdigest()[: self.len_prefix_memory]
        return uuid in self.parts[memory_prefix]

    def _store_in_memory(
        self, record_dict: Dict[str, Union[str, List[Dict[str, Any]]]]
    ):
        uuid = record_dict["uuid"]
        memory_prefix = md5(uuid.encode()).hexdigest()[: self.len_prefix_memory]
        self.parts[memory_prefix].add(uuid)

    def close(self):
        "Unlocks the log."
        lock_pth = self._log_lock_path
        if lock_pth.exists():
            lock_pth.unlink()
        self._locked = False

    def __del__(self):
        self.close()
