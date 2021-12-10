import re

from pytest import fixture, skip, mark
from dabapush.Configuration.FileWriterConfiguration import FileWriterConfiguration

@fixture
def writer_config() -> FileWriterConfiguration:
    return FileWriterConfiguration('test')

def test_make_file_name(writer_config: FileWriterConfiguration):
    regex = re.compile(r'(\d{2}-){3}\d{4}-test')
    writer_config.set_name_template('$name')
    name = writer_config.make_file_name()
    assert name == writer_config.name