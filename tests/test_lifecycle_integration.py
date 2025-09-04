"""Test suite for the Reader class and its backlog."""

import ujson

from dabapush import NDJSONReaderConfiguration, STDOUTWriterConfiguration
from dabapush.Backlog import Backlog
from dabapush.Lifecycle import LifecycleManager
from dabapush.Record import Record


def test_backlogging(monkeypatch, tmp_path):
    """
    Should write the records to a file if the log_path is set.
    """
    monkeypatch.chdir(tmp_path)  # Change the working directory to the temp path
    # to isolate the automatically created backlog.
    reader = NDJSONReaderConfiguration(
        "test", id="testing", read_path=str(tmp_path / "data"), pattern="*.json"
    ).get_instance()
    writer_config = STDOUTWriterConfiguration("test", id="testing", chunk_size=1)
    writer = writer_config.get_instance()
    back_log = Backlog(writer_config)
    manager = LifecycleManager(reader, writer, back_log)
    records = [{"key": f"value_{n}"} for n in range(3)]
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for file_num, record in enumerate(records):
        with (data_dir / f"test{file_num}.json").open("wt", encoding="utf8") as f:
            ujson.dump(record, f)  # pylint: disable=I1101

    manager.run()
    # reopen backlog
    back_log.load()
    for idx in range(3):
        assert Record(uuid=(data_dir / f"test{idx}.json:0").as_posix()) in back_log
