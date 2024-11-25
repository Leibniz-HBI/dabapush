"""Test the STDOUTWriter class."""
from dabapush import STDOUTWriterConfiguration


def test_stdout_writer(capsys):
    """Should write to stdout."""
    writer = STDOUTWriterConfiguration("stdout1").get_writer()
    writer.buffer = ["test"]
    writer.persist()

    captured = capsys.readouterr()
    assert captured.out == "test\n"
