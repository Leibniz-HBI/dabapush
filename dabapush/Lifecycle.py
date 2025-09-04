"""LifecycleManager class for connection Reader and writer while maintaining the backlog."""

from loguru import logger as log

from .Backlog import Backlog
from .Reader.Reader import Reader
from .Record import Record
from .Writer.Writer import Writer


class LifecycleManager:
    """Connects reader and writer while managing the backlog"""

    def __init__(self, reader: Reader, writer: Writer, back_log: Backlog):
        self.reader: Reader = reader
        self.writer: Writer = writer
        self.back_log: Backlog = back_log
        self.write_buffer = []
        self.read_records_of_group_offset = []
        self.error_uuids = set()
        self.chunk_size = writer.config.chunk_size

    def run(self):
        """Start processing.
        This will ingest records from the reader and store them using the writer.
        Records are only written if they have not been written before."""
        self.back_log.load()
        last_group_id = None
        last_group_offset = -1
        for record in self.reader.read():
            group_changed = record.group_id != last_group_id
            if group_changed or record.group_offset != last_group_offset:
                # write all records of previous group
                self._trigger_persist()
                # if possible compress backlog
                if len(self.error_uuids) == 0 and last_group_id is not None:
                    self.back_log.update_progress(
                        last_group_id,
                        last_group_offset,
                        self.read_records_of_group_offset,
                    )
                if group_changed:
                    self.error_uuids = set()
                self.read_records_of_group_offset = []
                last_group_offset = record.group_offset
                last_group_id = record.group_id
            self.read_records_of_group_offset.append(record)
            if record not in self.back_log:
                self.write_buffer.append(record)
            last_group_id = record.group_id
            if len(self.write_buffer) >= self.chunk_size:
                self._trigger_persist()
                if last_group_id is None:
                    # reader does not support grouping
                    self.read_records_of_group_offset = []
        self.back_log.close()

    def __del__(self):
        """Ensures the buffer is flushed before the object is destroyed."""
        self._trigger_persist()
        self.back_log.close()

    def _trigger_persist(self):
        if len(self.write_buffer) == 0:
            return
        write_errors = self.writer.write(self.write_buffer)
        if write_errors is None:
            write_errors = set()
        for record in self.write_buffer:
            if record.uuid in write_errors:
                log.error(f"Record {record.uuid} failed to be written.")
                self.error_uuids.add(record.uuid)
            else:
                log.debug(f"Setting record {record.uuid} as done.")
                record.done()
                self.log(record)
        self.write_buffer = []

    def log(self, record: Record):
        """Log the record to the persistent record log file."""
        self.back_log.write_record(record)

        log.debug(f"Done with {record.uuid}")
