"""Test suite for the Reader class and its backlog."""

from pathlib import Path

import ujson

from dabapush import NDJSONReaderConfiguration, STDOUTWriterConfiguration


def test_backlogging(monkeypatch, tmp_path):
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

    records = [{"key": f"value_{n}"} for n in range(3)]
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for file_num, record in enumerate(records):
        with (data_dir / f"test{file_num}.json").open("wt", encoding="utf8") as f:
            ujson.dump(record, f)  # pylint: disable=I1101

    writer.write(reader.read())

    log_path = Path(".dabapush/test/backlog")
    assert log_path.exists()
    content_count = 0
    for file_path in log_path.glob('*.jsonl'):
        with file_path.open("rt", encoding="utf8") as f:
            content_count += len(f.readlines())
    assert content_count  == len(records)
