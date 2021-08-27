from dabapush.Configuration.ProjectConfiguration import ProjectConfiguration
from dabapush.Configuration.Configuration import Configuration
import pytest


@pytest.fixture
def conf():
    project = ProjectConfiguration()
    project.initialize(Configuration())
    return 

def test_ProjectConfiguration(conf):
    pass
# should serialize
def test_serialize(conf):
    pass
# should deserialize
def test_deserialize(conf):
    pass
# should add reader plugin and assign it an ID and name
def test_add_reader(conf):
    id = conf.add_reader('Twacapic', 'name')

    assert 'Twacapic' in conf.readers

# should remove reader plugin by ID or by name
def test_remove_reader(conf):
    id = conf.add_reader('Twacapic', 'name')
    conf.remove_reader(id)

    assert not 'Twacapic' in conf.readers
# should list configured reader plugins
def test_list_reader(conf):
    pass
# should add writer plugins and assign it an ID and name
def test_add_writer(conf):
    pass
# should remove writer plugins by ID or name
def test_remove_writer(conf):
    pass
# should list configured writer plugins
def test_list_writers(conf):
    pass