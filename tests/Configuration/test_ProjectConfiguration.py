from collections import ChainMap
from pytest import fixture, skip
from dabapush.Configuration.ProjectConfiguration import ProjectConfiguration
from dabapush.Configuration.Configuration import Configuration
import pytest

@pytest.fixture
def conf() -> ProjectConfiguration:
    configuration = Configuration(
        ChainMap(        {
            "Twacapic": 'dabapush.Reader.TwacapicReader'
        })
    )
    project = ProjectConfiguration()
    project.initialize(configuration)
    return project

@fixture
def conf_loaded_single(conf: ProjectConfiguration) -> ProjectConfiguration:
    conf.add_reader('Twacapic', 'name')

    return conf

def test_ProjectConfiguration(conf):
    skip()
# should serialize
def test_serialize(conf):
    skip()
# should deserialize
def test_deserialize(conf):
    skip()
# should add reader plugin and assign it an ID and name
def test_add_reader(conf: ProjectConfiguration):
    id = conf.add_reader('Twacapic', 'name')

    assert 'name' in conf.readers

# should remove reader plugin by name
def test_remove_reader(conf_loaded_single: ProjectConfiguration):
    conf_loaded_single.remove_reader('name')

    assert 'name' not in conf_loaded_single.readers
# should list configured reader plugins
def test_list_reader(conf_loaded_single: ProjectConfiguration):
    entries = conf_loaded_single.list_readers()
    assert entries[0].name == 'name'
# should add writer plugins and assign it an ID and name
def test_add_writer(conf):
    skip()
# should remove writer plugins by ID or name
def test_remove_writer(conf):
    skip()
# should list configured writer plugins
def test_list_writers(conf):
    skip()