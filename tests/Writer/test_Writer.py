"""Tests for the Writer class."""

# pylint: disable=W0212, W0621, W0613, C0114, C0115, C0116
from pytest import fixture

from dabapush.Configuration.WriterConfiguration import WriterConfiguration
from dabapush.Record import Record
from dabapush.Writer.Writer import Writer


@fixture
def writer(isolated_test_dir) -> Writer:

    config = WriterConfiguration(name="test")
    return Writer(config)


def test_name(writer: Writer):
    assert writer.name == "test"


def test_id(writer: Writer):
    assert writer.id == writer.config.id


class MyTestWriter(Writer):
    def __init__(self, config):
        super().__init__(config)
        self.persisted_data = []

    def write(self, queue):
        self.persisted_data.extend((_.payload for _ in queue))


def test_writer_persist_method(isolated_test_dir):
    """Should persist the buffer."""

    config = WriterConfiguration(name="test", id=1, chunk_size=3)
    writer = MyTestWriter(config)
    queue = [Record(uuid=str(i), payload=i) for i in range(10)]
    writer.write(queue)
    assert writer.persisted_data == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
