"""Tests for the Writer class."""

# pylint: disable=W0212, W0621, C0114, C0115, C0116
from pytest import fixture

from dabapush.Configuration.WriterConfiguration import WriterConfiguration
from dabapush.Record import Record
from dabapush.Writer.Writer import Writer


@fixture
def writer(monkeypatch, tmp_path) -> Writer:
    monkeypatch.chdir(tmp_path)
    config = WriterConfiguration(name="test")
    return Writer(config)


def test_name(writer: Writer):
    assert writer.name == "test"


def test_id(writer: Writer):
    assert writer.id == writer.config.id


def test_writer_write_method(writer: Writer):
    """Should write to the buffer."""
    queue = (Record(i, uuid=str(i)) for i in range(10))
    writer.write(queue)
    assert [_.payload for _ in writer.buffer] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class MyTestWriter(Writer):
    def __init__(self, config):
        super().__init__(config)
        self.persisted_data = []

    def persist(self):
        self.persisted_data.extend((_.payload for _ in self.buffer))


def test_writer_persist_method(monkeypatch, tmp_path):
    """Should persist the buffer."""
    monkeypatch.chdir(tmp_path)

    config = WriterConfiguration(name="test", id=1, chunk_size=3)
    writer = MyTestWriter(config)
    queue = (Record(uuid=str(i), payload=i) for i in range(10))
    writer.write(queue)
    writer._trigger_persist()
    assert writer.persisted_data == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert not writer.buffer


def test_writer_persist_method_with_backlog(monkeypatch, tmp_path):
    """Should persist the buffer."""
    monkeypatch.chdir(tmp_path)

    config = WriterConfiguration(name="test", id=1, chunk_size=3)
    queue = [Record(uuid=str(i), payload=i) for i in range(10)]
    writer = MyTestWriter(config)
    writer.write((_ for _ in queue))
    writer._trigger_persist()

    del writer

    writer = MyTestWriter(config)
    writer._trigger_persist()

    assert not writer.persisted_data
    assert not writer.buffer
    assert len(writer.back_log) == 10
    assert all(_.uuid == str(i) for i, _ in enumerate(writer.back_log))
