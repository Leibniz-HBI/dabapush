from pytest import fixture, skip, mark
from dabapush.Configuration.Configuration import Configuration

@fixture
def conf():
    return Configuration({
        'twacapic': 'some.garbage',
        'factli': 'some.other.garbage'},
    {
        'twacapic': 'some.garbage',
        'factli': 'some.other.garbage'
    })

# should serialize
def test_serialize(conf: Configuration):
    skip()
# should deserialize
def test_deserialize(conf: Configuration):
    skip()
# should get a reader plugin and return it
def test_get_reader(conf: Configuration):
    assert conf.get_reader('twacapic') is not None
# should register a reader plugin and assign it a name
def test_register_reader(conf: Configuration):
    conf.register_reader('doopy', 'snoopy')

    assert 'doopy' in conf.readers
# should remove reader plugin by name
def test_remove_reader(conf: Configuration):
    skip()
# should list registered reader plugins
def test_list_reader(conf: Configuration):
    skip()
# should register writer plugins and assign a name
def test_register_writer(conf: Configuration):
    skip()
# should remove writer plugins by name
def test_remove_writer(conf: Configuration):
    skip()
# should list registered writer plugins
def test_list_writers(conf: Configuration):
    skip()
# should get a writer plugin and return it
def test_get_writer(conf: Configuration):
    assert conf.get_writer('twacapic') is not None
# should union two disjunct configuratuions
def test_merge_configurations(conf: Configuration):
    skip()