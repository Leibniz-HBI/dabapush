"""Test suite for dabapush.FacebookDBWriterConfiguration and dabapush.Writer.FacebookDBWriter."""
from dabapush import FacebookDBWriterConfiguration
from dabapush.Writer.Writer import Writer

conf = FacebookDBWriterConfiguration("default", password="postgres", dbname="postgres")


def test_intializer():
    """Should import and instantiate correctly."""
    assert isinstance(conf.get_instance(), Writer)
