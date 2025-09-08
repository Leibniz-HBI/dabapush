"""LifecycleManager class for connection Reader and writer while maintaining the backlog."""

from loguru import logger as log

from .Backlog import AlreadyProgressedException, Backlog
from .Reader.Reader import ProgressInvalidException, Reader
from .Record import Record
from .utils import Timer
from .Writer.Writer import Writer


class LifecycleManager:  # pylint: disable=too-many-instance-attributes
    """Connects reader and writer while managing the backlog

    Attributes
    ----------
    reader : Reader
        The reader instance to read records from.
    writer : Writer
        The writer instance to write records to.
    back_log : Backlog
        The backlog instance to keep track of processed records."""

    def __init__(self, reader: Reader, writer: Writer, back_log: Backlog):
        self.reader: Reader = reader
        self.writer: Writer = writer
        self.back_log: Backlog = back_log
        self.write_buffer = []
        self.read_records_of_group_offset = []
        self.error_uuids = set()
        self.chunk_size = writer.config.chunk_size
        self._timer = Timer(micros=100000)  # 100 ms timer for reading

    def run(self):
        """Start processing.
        This will ingest records from the reader and store them using the writer.
        Records are only written if they have not been written before."""
        self.back_log.load()
        last_group_id = None
        last_group_offset = -1
        self._timer.mark()
        for record in self.reader.read():
            group_changed = record.group_progress.group_id != last_group_id
            if group_changed or record.group_progress.group_offset != last_group_offset:
                # write all records of previous group
                self._trigger_persist()
                # if possible compress backlog
                if (
                    len(self.error_uuids) == 0
                    and last_group_id is not None
                    and self._timer.ok()
                ):
                    self.back_log.update_progress(
                        last_group_id,
                        last_group_offset,
                        self.read_records_of_group_offset,
                    )
                if group_changed:
                    self.error_uuids = set()
                self.read_records_of_group_offset = []
                last_group_offset = record.group_progress.group_offset
                last_group_id = record.group_progress.group_id
            self.read_records_of_group_offset.append(record)
            try:
                do_write = not record in self.back_log
            except AlreadyProgressedException as exc:
                # Backlog says record group was already processed
                try:
                    self.reader.set_progress(exc.group_id, exc.group_offset)
                    do_write = False
                    last_group_id = None
                    last_group_offset = -1
                except ProgressInvalidException:
                    # Reader says underlying source has changed, therefore progress is invalid.
                    self.back_log.update_progress(
                        record.group_progress.group_id, -1, []
                    )
                    do_write = True
            if do_write:
                self.write_buffer.append(record)
            if len(self.write_buffer) >= self.chunk_size:
                self._trigger_persist()
                if last_group_id is None:
                    # reader does not support grouping
                    self.read_records_of_group_offset = []
        # write last progress.
        if last_group_id is not None and len(self.error_uuids) == 0:
            self.back_log.update_progress(
                last_group_id, last_group_offset, self.read_records_of_group_offset
            )
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
