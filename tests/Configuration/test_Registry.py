"""Test suite for dabapush.Configuration.Registry."""
# pylint: disable=W0621
import pytest
from pytest import fixture, skip

from dabapush.Configuration.ProjectConfiguration import ProjectConfiguration
from dabapush.Configuration.Registry import Registry


@pytest.fixture
def conf() -> ProjectConfiguration:
    """Provide a ProjectConfiguration."""
    reg = Registry()

    print(reg.list_all_readers())

    return ProjectConfiguration()


@fixture
def conf_loaded_single_reader(conf: ProjectConfiguration) -> ProjectConfiguration:
    """Provide a ProjectConfiguration with exactly one Reader."""
    conf.add_reader("Twacapic", "name")

    return conf


@fixture
def conf_loaded_single_writer(conf: ProjectConfiguration) -> ProjectConfiguration:
    """Provide a ProjectConfiguration with exactly one Writer."""
    conf.add_writer("CSV", "name")
    return conf


def test_serialize():
    """Should serialize."""
    skip()


def test_deserialize():
    """Should deserialize."""
    skip()


def test_add_reader(conf: ProjectConfiguration):
    """Should add reader plugin and assign it an ID and name."""
    conf.add_reader("Twacapic", "name")
    assert "name" in conf.readers


def test_remove_reader(conf_loaded_single_reader: ProjectConfiguration):
    """Should remove reader plugin by name."""
    conf_loaded_single_reader.remove_reader("name")

    assert "name" not in conf_loaded_single_reader.readers


def test_list_reader(conf_loaded_single_reader: ProjectConfiguration):
    """Should list configured reader plugins."""
    entries = conf_loaded_single_reader.list_readers()
    assert "name" in [_.name for _ in entries]


def test_add_writer(conf: ProjectConfiguration):
    """Should add writer plugins and assign it an ID and name."""
    conf.add_writer("CSV", "name")
    assert "name" in conf.writers


def test_remove_writer(conf_loaded_single_writer: ProjectConfiguration):
    """Should remove writer plugins by ID or name."""
    conf_loaded_single_writer.remove_writer("name")

    assert "name" not in conf_loaded_single_writer.writers


def test_list_writers(conf_loaded_single_writer: ProjectConfiguration):
    """Should list configured writer plugins."""
    ret = conf_loaded_single_writer.list_writers()

    assert "name" == ret[0].name


def test_initialize():
    """Should raise an Exception if accessed prematurely."""
    # we expect ProjectConfig to raise an exception
    # if accessed before intializiation
    raised = False
    try:
        project = ProjectConfiguration()
        project.add_reader("Thing", "thing")
    except BaseException:
        raised = True

    assert raised is True
