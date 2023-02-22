"""Test suite for dabapush.InstagramDBWriterConfiguration and dabapush.Writer.InstagramDBWriter."""
from dabapush import InstagramDBWriterConfiguration
from dabapush.Writer.Writer import Writer

conf = InstagramDBWriterConfiguration("default", password="postgres", dbname="postgres")


def test_intializer():
    """Should import and instantiate correctly."""
    assert isinstance(conf.get_instance(), Writer)
