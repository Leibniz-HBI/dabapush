from pytest import fixture, skip
from dabapush.Configuration.ProjectConfiguration import ProjectConfiguration
from dabapush.Configuration.Registry import Registry
import pytest
import yaml


@pytest.fixture
def conf() -> ProjectConfiguration:
    Registry()

    return ProjectConfiguration()


@fixture
def conf_loaded_single_reader(conf: ProjectConfiguration) -> ProjectConfiguration:
    conf.add_reader("Twacapic", "name")

    return conf


@fixture
def conf_loaded_single_writer(conf: ProjectConfiguration) -> ProjectConfiguration:
    conf.add_writer("CSV", "name")
    return conf


# should serialize
def test_serialize(conf: ProjectConfiguration):
    skip()
    thing = yaml.dump(conf)
    print(thing)


# should deserialize
def test_deserialize(conf):
    skip()


# should add reader plugin and assign it an ID and name
def test_add_reader(conf: ProjectConfiguration):
    id = conf.add_reader("Twacapic", "name")
    assert "name" in conf.readers


# should remove reader plugin by name
def test_remove_reader(conf_loaded_single_reader: ProjectConfiguration):
    conf_loaded_single_reader.remove_reader("name")

    assert "name" not in conf_loaded_single_reader.readers


# should list configured reader plugins
def test_list_reader(conf_loaded_single_reader: ProjectConfiguration):
    entries = conf_loaded_single_reader.list_readers()
    assert entries[0].name == "name"


# should add writer plugins and assign it an ID and name
def test_add_writer(conf: ProjectConfiguration):
    conf.add_writer("CSV", "name")
    assert "name" in conf.writers


# should remove writer plugins by ID or name
def test_remove_writer(conf_loaded_single_writer: ProjectConfiguration):
    conf_loaded_single_writer.remove_writer("name")

    assert "name" not in conf_loaded_single_writer.writers


# should list configured writer plugins
def test_list_writers(conf_loaded_single_writer: ProjectConfiguration):
    ret = conf_loaded_single_writer.list_writers()

    assert "name" == ret[0].name


def test_initialize():
    # we expect ProjectConfig to raise an exception
    # if accessed bfore intializiation
    raised = False
    try:
        p = ProjectConfiguration()
        p.add_reader("Thing", "thing")
    except:
        raised = True

    assert raised == True
