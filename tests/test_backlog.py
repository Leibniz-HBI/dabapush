# pylint: disable=redefined-outer-name,protected-access,unused-argument
"""Test for the Backlog"""
from pathlib import Path
from dabapush.Backlog import Backlog, BacklogLockedException
from dabapush.Configuration.WriterConfiguration import WriterConfiguration
from dabapush.Record import Record

import pytest

from ujson import dump, loads

name_writer = "backlog_writer_for_test"


@pytest.fixture
def writer_config():
    "A simple writer configuration for tests"
    return WriterConfiguration(name=name_writer)


@pytest.fixture
def uuids():
    return [f"uuid_{idx:02d}" for idx in range(20)]


@pytest.fixture
def existing_log(isolated_test_dir, uuids):
    dabapush_dir = Path('.dabapush')
    dabapush_dir.mkdir()
    with open(dabapush_dir/f"{name_writer}.jsonl", "wt", encoding="utf8") as test_file:
        for uuid in uuids:
            dump({"uuid": uuid}, test_file)
            test_file.write("\n")


def test_contains_empty_parts(writer_config):
    "Record missing from backlog is correctly reported."
    backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    record = Record(uuid="some_id")
    assert record not in backlog


def test_contains(writer_config):
    "Record present in the backlog is correctly reported."
    backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    record = Record(uuid="some_id")
    backlog._store_in_memory(record.to_log())
    assert record in backlog


def test_conversion(existing_log,  writer_config):
    "Test the conversion from old log format to new log format."
    backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    backlog.load()
    dabapush_pth = Path(".dabapush")
    old_log_path = dabapush_pth / f"{name_writer}.jsonl"
    assert not old_log_path.exists()
    log_dir = dabapush_pth / name_writer/"backlog"
    assert log_dir.is_dir()
    all_uuids = []
    for pth in log_dir.glob('*.jsonl'):
        with pth.open("rt", encoding="utf8") as part_file:
            for line in part_file.readlines():
                json = loads(line)
                uuid = json["uuid"]
                all_uuids.append(uuid)
    assert len(all_uuids) == 20
    assert len(set(all_uuids)) == 20

def test_write_and_load_backlog(uuids, isolated_test_dir, writer_config):
    "Test reopening a backlog"
    backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    backlog.load()
    for uuid in uuids:
        backlog.write_record(Record(uuid=uuid))
    all_uuids = []
    for _part, uuid_set in backlog.parts.items():
        for uuid in uuid_set:
            all_uuids.append(uuid)
    assert len(all_uuids) ==20
    all_uuid_set = set(all_uuids)
    assert len(all_uuid_set) == 20
    backlog.close()
    read_backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    read_backlog.load()
    all_read_uuids = []
    for _part, uuid_set in backlog.parts.items():
        for uuid in uuid_set:
            all_read_uuids.append(uuid)
    assert len(all_read_uuids)==20
    assert set(all_read_uuids) == all_uuid_set



def test_does_not_open_when_locked(isolated_test_dir, writer_config):
    "Make sure a locked backlog is not loaded."
    backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    backlog.load()
    read_backlog = Backlog(
        len_prefix_persist=2, len_prefix_memory=2, writer_config=writer_config
    )
    with pytest.raises(BacklogLockedException):
        read_backlog.load()