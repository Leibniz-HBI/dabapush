from Configuration.ConfigurationError import ConfigurationError
from tests.Configuration.test_ProjectConfiguration import conf
from typing import List
import yaml

from Configuration.Configuration import Configuration

class ProjectConfiguration(yaml.YAMLObject):
    def __init__(self) -> None:
        super().__init__()

        self.readers: List(ReaderConfiguration) = []
        self.writers: List(WriterConfiguration) = []
        self.configuration: Configuration

    def __repr__(self) -> str:
        return super().__repr__()

    def add_reader(self, type: str, name: str):
        # check wether global/local configuration is set up
        if (self.is_initialized == True): 
            pass
        else:
            raise ConfigurationError()
        # get constructor from registry
        constructor = self.configuration.get_reader(type)
        # instantiate with name
        instance = constructor(name)
        self.writers.reader.append(instance)
        # return id
        return instance.id

    def remove_reader(name: str):
        pass

    def list_readers():
        pass

    def add_writer(type: str, name: str):
        pass

    def remove_writer(name: str):
        pass

    def list_writers():
        pass

    @property
    def is_initialized(self) -> bool:
        return self.configuration is not None

    def initialize(self, conf: Configuration) -> None:
        self.configuration = conf