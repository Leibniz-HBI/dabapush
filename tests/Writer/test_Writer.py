from pytest import fixture, skip, mark
from dabapush.Writer.Writer import Writer
from dabapush.Configuration.WriterConfiguration import WriterConfiguration


@fixture
def writer() -> Writer:
    config = WriterConfiguration(name="test")
    return Writer(config)


def test_name(writer: Writer):
    assert writer.name == "test"


def test_id(writer: Writer):
    assert writer.id == writer.config.id
