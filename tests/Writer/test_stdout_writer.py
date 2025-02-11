"""Test the STDOUTWriter class."""

from dabapush import STDOUTWriterConfiguration
from dabapush.Record import Record


def test_stdout_writer(capsys, isolated_test_dir):  # pylint: disable=unused-argument
    """Should write to stdout."""
    writer = STDOUTWriterConfiguration("stdout1").get_instance()
    writer.buffer = [Record(uuid="test.01", source=None, payload="test")]
    writer.persist()

    captured = capsys.readouterr()
    assert captured.out == "test\n"
