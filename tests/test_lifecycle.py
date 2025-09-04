"""Tests for the lifecycle manager."""

# pylint: disable=redefined-outer-name
from unittest.mock import MagicMock, call

from pytest import fixture

from dabapush.Lifecycle import LifecycleManager
from dabapush.Record import Record


@fixture
def lifecycle_controller_with_mocks():
    """A lifecycle controller with mocked reader, writer and backlog."""
    reader = MagicMock()
    writer = MagicMock()
    writer.config.chunk_size = 2
    writer.persist = MagicMock(return_value=None)
    backlog = MagicMock()
    backlog.write_record = MagicMock()
    return LifecycleManager(reader=reader, writer=writer, back_log=backlog)


def mk_records(end, group_id=None, sub_group_size=5):
    """Create a list of records with uuids from start to end-1."""
    if group_id is None:

        def group_offset_func(_):  # pylint: disable=missing-function-docstring
            return None

    else:

        def group_offset_func(i):  # pylint: disable=missing-function-docstring
            return i // sub_group_size

    return [
        Record(uuid=str(i), group_id=group_id, group_offset=group_offset_func(i))
        for i in range(0, end)
    ]


def test_lifecycle_run_triggers_persist(lifecycle_controller_with_mocks):
    """Make sure records are persisted when chunk size is reached."""
    controller = lifecycle_controller_with_mocks
    records = mk_records(2)
    controller.reader.read.return_value = (x for x in records)
    controller.run()
    controller.writer.write.assert_called_with(records)
    assert controller.write_buffer == []
    assert controller.read_records_of_group_offset == []
    controller.back_log.write_record.assert_has_calls(
        [call(records[0]), call(records[1])]
    )


def test_keeps_read_records_with_grouped(lifecycle_controller_with_mocks):
    """Make sure read records are kept when reading from grouped reader."""
    controller = lifecycle_controller_with_mocks
    records = mk_records(2, group_id="group1")
    controller.reader.read.return_value = (x for x in records)
    controller.run()
    controller.writer.write.assert_called_with(records)
    assert controller.read_records_of_group_offset == records


def test_backlog_progress_updated_on_group_change(lifecycle_controller_with_mocks):
    """Make sure backlog progress is updated when group changes."""
    controller = lifecycle_controller_with_mocks
    records = mk_records(2, group_id="group1") + mk_records(1, group_id="group2")
    controller.reader.read.return_value = (x for x in records)
    controller.run()
    controller.back_log.update_progress.assert_called_with(
        "group1", 0, [records[0], records[1]]
    )
    assert controller.read_records_of_group_offset == [records[2]]


def test_does_not_update_progress_with_errors(lifecycle_controller_with_mocks):
    """Make sure backlog progress is not updated when there are write errors."""
    controller = lifecycle_controller_with_mocks
    records = mk_records(2, group_id="group1") + mk_records(1, group_id="group2")
    controller.reader.read.return_value = (x for x in records)
    controller.writer.write.side_effect = [{records[1].uuid}, {}]
    controller.run()
    controller.back_log.update_progress.assert_not_called()
    controller.back_log.write_record.assert_called_once_with(records[0])
    assert controller.read_records_of_group_offset == [records[2]]
    assert controller.error_uuids == set()


def test_backlog_progress_updated_on_offset_change(lifecycle_controller_with_mocks):
    """Make sure backlog progress is updated when group offset changes."""
    controller = lifecycle_controller_with_mocks
    records = mk_records(3, group_id="group1", sub_group_size=2)
    controller.reader.read.return_value = (x for x in records)
    controller.run()
    controller.back_log.update_progress.assert_called_with(
        "group1", 0, [records[0], records[1]]
    )
    assert controller.read_records_of_group_offset == [records[2]]


def test_errors_not_cleared_on_offset_change(lifecycle_controller_with_mocks):
    """Make sure write errors are not cleared when group offset changes."""
    controller = lifecycle_controller_with_mocks
    records = mk_records(3, group_id="group1", sub_group_size=2)
    controller.reader.read.return_value = (x for x in records)
    controller.writer.write.side_effect = [{records[1].uuid}, {}]
    controller.run()
    controller.back_log.update_progress.assert_not_called()
    controller.back_log.write_record.assert_called_once_with(records[0])
    assert controller.read_records_of_group_offset == [records[2]]
    assert controller.error_uuids == {records[1].uuid}


def test_persist_on_controller_destruction(lifecycle_controller_with_mocks):
    """Should persist the buffer."""

    controller = lifecycle_controller_with_mocks
    records = mk_records(1)
    reader = controller.reader
    reader.read.return_value = (x for x in records)
    controller.run()

    writer = controller.writer
    writer.write.assert_not_called()
    back_log = controller.back_log
    back_log.write_record.assert_not_called()

    controller.__del__()  # pylint: disable=unnecessary-dunder-call
    writer.write_called_once_with(records)
    back_log.write_record.assert_called_once_with(records[0])
    back_log.close.assert_has_calls([call(), call()])  # once in run and once in del
