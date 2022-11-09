"""Test suite for dabapush.Configuration.Configuration."""
# pylint: disable=W0621
from pytest import fixture, skip

from dabapush.Configuration.Registry import Registry


@fixture
def conf():
    """Provide a Registry."""
    return Registry()


# should serialize
def test_serialize():
    """Should serialize the configuration"""
    skip()


# should deserialize
def test_deserialize():
    """Should deserialize the configuration"""
    skip()


# should get a reader plugin and return it
def test_get_reader(conf: Registry):
    """Should successfully get a ReaderConfiguration from the registry."""
    assert conf.get_reader("Twacapic") is not None


# should remove reader plugin by name
def test_remove_reader():
    """Should do something, I guess."""
    skip()


# should list registered reader plugins
def test_list_reader():
    """Should do something, I guess."""
    skip()


# should register writer plugins and assign a name
def test_register_writer():
    """Should do something, I guess."""
    skip()


# should remove writer plugins by name
def test_remove_writer():
    """Should do something, I guess."""
    skip()


# should list registered writer plugins
def test_list_writers():
    """Should do something, I guess."""
    skip()


# should get a writer plugin and return it
def test_get_writer(conf: Registry):
    """Should successfully get a WriterConfiguration from the registry."""
    assert conf.get_writer("CSV") is not None
