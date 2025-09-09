# pylint: disable=redefined-outer-name,protected-access,unused-argument,c-extension-no-member
"""Test for the Backlog"""
import dbm
from datetime import datetime
from pathlib import Path
from shutil import copy
from unittest.mock import MagicMock, patch

import pytest
import ujson

from dabapush.Backlog import AlreadyProgressedException, Backlog, BacklogLockedException
from dabapush.Configuration.WriterConfiguration import WriterConfiguration
from dabapush.Record import Record
from dabapush.utils import Progress

name_writer = "backlog_writer_for_test"


@pytest.fixture
def writer_config():
    """A simple writer configuration for tests"""
    return WriterConfiguration(name=name_writer, chunk_size=2)


@pytest.fixture
def uuids():
    """Fixture providing a list of uuids."""
    return [f"uuid_{idx:02d}" for idx in range(20)]


@pytest.fixture
def existing_log(isolated_test_dir, uuids):
    """Fixture providing a log in the old ndjson format."""
    dabapush_dir = Path(".dabapush")
    dabapush_dir.mkdir()
    with open(
        dabapush_dir / f"{name_writer}.jsonl", "wt", encoding="utf8"
    ) as test_file:
        for uuid in uuids:
            ujson.dump({"uuid": uuid}, test_file)
            test_file.write("\n")


@pytest.fixture
def get_existing_backlog_path():
    """Fixture providing a path to an existing gdbm backlog."""
    yield (Path(__file__).parent / "stubs/test_database_gdbm").resolve()


@pytest.fixture
def existing_gdbm_backlog(isolated_test_dir, get_existing_backlog_path):
    """Fixture providing a gdbm backlog."""
    file_name = "backlog.db"
    db_pth = Path(".dabapush") / name_writer / "backlog"
    db_pth.mkdir(parents=True)
    copy(get_existing_backlog_path, db_pth / file_name)

    yield True


def test_contains_empty_parts(writer_config, isolated_test_dir):
    """Record missing from backlog is correctly reported."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    record = Record(uuid="missing_id")
    assert record not in backlog


def test_contains(writer_config, isolated_test_dir):
    """Record present in the backlog is correctly reported."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    record = Record(uuid="some_id")
    backlog.write_record(record)
    assert record in backlog


def test_contains_progress(writer_config, isolated_test_dir):
    """Record present in backlog as progress entry is reported as present."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    group_id = "group"
    backlog.update_progress(group_id, 1, [])
    record = Record(uuid="some_id", group_progress=Progress(group_id, 1))
    with pytest.raises(AlreadyProgressedException) as exc:
        record in backlog  # pylint: disable=pointless-statement
    assert exc.value.group_id == group_id
    assert exc.value.group_offset == 1


def test_contains_progress_falls_back_to_uuid_missing(writer_config, isolated_test_dir):
    """Record present in backlog as progress entry is reported as present."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    group_id = "group"
    backlog.update_progress(group_id, 1, [])
    record = Record(uuid="some_id", group_progress=Progress(group_id, 2))
    assert record not in backlog


def test_contains_progress_falls_back_to_uuid_present(writer_config, isolated_test_dir):
    """Record present in backlog as progress entry is reported as present."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    group_id = "group"
    backlog.update_progress(group_id, 1, [])
    record = Record(uuid="some_id", group_progress=Progress(group_id, 2))
    backlog.write_record(record)
    assert record in backlog


def test_update_progress_deletes_records(writer_config, isolated_test_dir):
    """Updating progress deletes records with lower or equal group offset."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    group_id = "group"
    records = [
        Record(uuid=f"some_id_{i}", group_progress=Progress(group_id, 2))
        for i in range(5)
    ]
    for record in records:
        backlog.write_record(record)
    backlog.update_progress(group_id, 2, records)
    for record in records:
        assert record.uuid not in backlog._db_connection
        with pytest.raises(AlreadyProgressedException) as exc:
            assert record in backlog
        assert exc.value.group_id == group_id
        assert exc.value.group_offset == 2
    assert backlog.get_progress(group_id) == 2


def test_last_progress_cache(writer_config):
    """Make sure the last progress dict is used to avoid db calls."""
    backlog = Backlog(writer_config=writer_config)
    backlog._locked = True
    backlog._db_connection = MagicMock()
    backlog._last_progress_dict = {"uuid": "group1", "max_group_offset": 3}
    progress = backlog.get_progress("group1")
    assert progress == 3
    backlog._db_connection.__contains__.assert_not_called()


def test_does_revert_progress(writer_config, isolated_test_dir):
    """Make sure progress is not reverted when updating with lower offset."""
    backlog = Backlog(writer_config=writer_config)
    backlog._locked = True
    backlog._db_connection = MagicMock()
    group_id = "group1"
    timestamp = datetime(2024, 1, 1, 12, 0, 0)
    timestamp_str = timestamp.isoformat()
    backlog._db_connection.get.return_value = ujson.dumps(
        {"uuid": group_id, "max_group_offset": 2, "processed_at": timestamp_str}
    )
    mock = MagicMock()
    mock.now.return_value = timestamp
    with patch("dabapush.Backlog.datetime", mock):
        backlog.update_progress(group_id, 1, [])
    assert backlog.get_progress(group_id) == 1
    backlog._db_connection.__setitem__.assert_called_once_with(
        group_id,
        ujson.dumps(
            {"uuid": group_id, "max_group_offset": 1, "processed_at": timestamp_str}
        ),
    )


def test_conversion(existing_log, writer_config, isolated_test_dir):
    """Test the conversion from old log format to new log format."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()

    del backlog

    dabapush_pth = Path(".dabapush")
    old_log_path = dabapush_pth / f"{name_writer}.jsonl"
    assert not old_log_path.exists()
    assert old_log_path.with_suffix(".jsonl.old").exists()
    db_pth = dabapush_pth / name_writer / "backlog" / "backlog.db"
    assert db_pth.is_file()
    all_uuids = dbm.open(db_pth.as_posix(), "r").keys()
    assert len(all_uuids) == 20
    assert len(set(all_uuids)) == 20


def test_write_and_load_backlog(uuids, isolated_test_dir, writer_config):
    """Test reopening a backlog"""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    for uuid in uuids:
        backlog.write_record(Record(uuid=uuid))
    backlog.close()

    read_backlog = Backlog(writer_config=writer_config)
    read_backlog.load()

    for uuid in uuids:
        assert Record(uuid=uuid) in read_backlog


def test_load_old_backlog(uuids, existing_gdbm_backlog, writer_config):
    """Test reopening a backlog"""
    read_backlog = Backlog(writer_config=writer_config)
    read_backlog.load()

    for uuid in uuids:
        assert Record(uuid=uuid) in read_backlog


def test_does_not_open_when_locked(isolated_test_dir, writer_config):
    """Make sure a locked backlog is not loaded."""
    backlog = Backlog(writer_config=writer_config)
    backlog.load()
    read_backlog = Backlog(writer_config=writer_config)
    with pytest.raises(BacklogLockedException):
        read_backlog.load()
