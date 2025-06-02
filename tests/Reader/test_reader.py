"""Test suite for the Reader class and its backlog."""

import ujson

from dabapush import NDJSONReaderConfiguration, STDOUTWriterConfiguration
from dabapush.Record import Record


def test_backlogging(monkeypatch, tmp_path, n=10):
    """
    Should write the records to a file if the log_path is set.
    """
    monkeypatch.chdir(tmp_path)  # Change the working directory to the temp path
    # to isolate the automatically created backlog.
    reader = NDJSONReaderConfiguration(
        "test", id="testing", read_path=str(tmp_path / "data"), pattern="*.json"
    ).get_instance()
    writer = STDOUTWriterConfiguration(
        "test", id="testing", chunk_size=1
    ).get_instance()

    records = [{"key": f"value_{n}"} for n in range(n)]
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for file_num, record in enumerate(records):
        with (data_dir / f"test{file_num}.json").open("wt", encoding="utf8") as f:
            ujson.dump(record, f)  # pylint: disable=I1101

    writer.write(reader.read())
    for idx in range(n):
        assert (
            Record(uuid=(data_dir / f"test{idx}.json:17").as_posix()) in writer.back_log
        )
