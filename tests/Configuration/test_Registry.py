from importlib.metadata import EntryPoint

from dabapush.Configuration import Registry


def test_readers():
    readers = Registry.readers()

    assert isinstance(readers, tuple)
    assert all(isinstance(_, EntryPoint) for _ in readers)


def test_writers():
    writers = Registry.writers()

    assert isinstance(writers, tuple)
    assert all(isinstance(_, EntryPoint) for _ in writers)
