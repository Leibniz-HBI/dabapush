"""Test suite for the Reader class and its backlog."""

from os import remove

import pytest
import ujson

from dabapush import NDJSONReaderConfiguration, STDOUTWriterConfiguration
from dabapush.Backlog import Backlog
from dabapush.Lifecycle import AlreadyProgressedException, LifecycleManager
from dabapush.Record import Record
from dabapush.utils import Progress


def assert_progress(back_log: Backlog, group_id, expected_progress):
    "Test that the correct progress is contained in the backlog."
    with pytest.raises(AlreadyProgressedException) as exc:
        Record(  # pylint: disable=expression-not-assigned
            uuid="empty", group_progress=Progress(group_id, 0)
        ) in back_log
    assert exc.value.group_offset == expected_progress


def test_backlogging(monkeypatch, tmp_path, capsys):
    """
    Should write the records to a file if the log_path is set.
    """
    monkeypatch.chdir(tmp_path)  # Change the working directory to the temp path
    # to isolate the automatically created backlog.
    writer_config = STDOUTWriterConfiguration("test", id="testing", chunk_size=1)
    back_log = Backlog(writer_config)
    manager = LifecycleManager(
        NDJSONReaderConfiguration(
            "test", id="testing", read_path=str(tmp_path / "data"), pattern="*.json"
        ).get_instance(),
        writer_config.get_instance(),
        back_log,
    )
    manager._timer.micros = 1  # pylint: disable=protected-access
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
        assert_progress(back_log, (data_dir / f"test{idx}.json").as_posix(), 17)
    captured_output = capsys.readouterr()
    assert captured_output.out == "\n".join(
        [
            "{'key': 'value_2'}",
            "{'key': 'value_1'}",
            "{'key': 'value_0'}\n",
        ]
    )


def test_resets_progress_for_overwritten_files(monkeypatch, tmp_path, capsys):
    """
    Should reset the progress if a file is overwritten with a smaller file.
    """
    monkeypatch.chdir(tmp_path)  # Change the working directory to the temp path
    # to isolate the automatically created backlog.
    writer_config = STDOUTWriterConfiguration("test", id="testing", chunk_size=1)
    back_log = Backlog(writer_config)
    manager = LifecycleManager(
        NDJSONReaderConfiguration(
            "test", id="testing", read_path=str(tmp_path / "data"), pattern="*.json"
        ).get_instance(),
        writer_config.get_instance(),
        back_log,
    )
    manager._timer.micros = 1  # pylint: disable=protected-access
    # value needs to be longer to allow for detection of overwrite.
    records = [{"key": f"value_{n}"} for n in range(3)]
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for file_num, record in enumerate(records):
        path = data_dir / f"test{file_num}.json"
        with (path).open("wt", encoding="utf8") as f:
            ujson.dump(record, f)  # pylint: disable=I1101

    manager.run()
    back_log.load()
    assert_progress(back_log, (data_dir / "test1.json").as_posix(), 17)
    back_log.close()
    # overwrite one of the files with smaller content
    file_1_path = data_dir / "test1.json"
    remove(file_1_path)
    captured_output = capsys.readouterr()
    assert "{'key': 'value_1'}\n" in captured_output.out
    with (file_1_path).open("wt", encoding="utf8") as f:
        ujson.dump({"key": "new"}, f)  # pylint: disable=I1101

    manager.run()
    # reopen backlog
    back_log.load()
    assert_progress(back_log, (data_dir / "test1.json").as_posix(), 13)
    captured_output = capsys.readouterr()
    assert captured_output.out == "{'key': 'new'}\n"
