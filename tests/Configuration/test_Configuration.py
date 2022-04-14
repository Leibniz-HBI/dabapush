from pytest import fixture, skip, mark
from Configuration.Registry import Registry
from dabapush.Configuration.ReaderConfiguration import ReaderConfiguration


@fixture
def conf():
    return Registry(
        {"twacapic": "some.garbage", "factli": "some.other.garbage"},
        {"twacapic": "some.garbage", "factli": "some.other.garbage"},
    )


# should serialize
def test_serialize(conf: Registry):
    skip()


# should deserialize
def test_deserialize(conf: Registry):
    skip()


# should get a reader plugin and return it
def test_get_reader(conf: Registry):
    assert conf.get_reader("twacapic") is not None


# should register a reader plugin and assign it a name
def test_register_reader(conf: Registry):
    class Blub(ReaderConfiguration):
        def __init__(self, name, id) -> None:
            super().__init__(name, id=id)

    conf.register_reader("doopy", Blub)

    assert "doopy" in conf.readers


# should remove reader plugin by name
def test_remove_reader(conf: Registry):
    skip()


# should list registered reader plugins
def test_list_reader(conf: Registry):
    skip()


# should register writer plugins and assign a name
def test_register_writer(conf: Registry):
    skip()


# should remove writer plugins by name
def test_remove_writer(conf: Registry):
    skip()


# should list registered writer plugins
def test_list_writers(conf: Registry):
    skip()


# should get a writer plugin and return it
def test_get_writer(conf: Registry):
    assert conf.get_writer("twacapic") is not None


# should union two disjunct configuratuions
def test_merge_configurations(conf: Registry):
    skip()
