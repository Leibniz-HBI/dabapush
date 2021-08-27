import yaml
from typing import List
from .ConfigurationError import ConfigurationError
from .Configuration import Configuration
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


class ProjectConfiguration(yaml.YAMLObject):
    def __init__(self, readers=[] , writers=[]) -> None:
        super().__init__()

        # store readers if they are passed into the constructor or else intialize new list
        self.readers: List(ReaderConfiguration) = readers
        # store writers if they are passed into the constructor or else intialize new list
        self.writers: List(WriterConfiguration) = writers
        # the global and/or local configurations are sepratedly stored objects and are, thus,
        # not deserialized and requiere further setup in our class, see property `self.is_initialized`
        # and method `self.initialize()`.
        self.configuration: Configuration = None

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


    # pass a global/local/merged configuration to the project
    def initialize(self, conf: Configuration) -> None:
        self.configuration = conf