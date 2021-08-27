import yaml
from typing import List, Mapping
from .ConfigurationError import ConfigurationError
from .Configuration import Configuration
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


class ProjectConfiguration(yaml.YAMLObject):
    def __init__(
            self,
            readers: Mapping[str, ReaderConfiguration] = {},
            writers: Mapping[str, WriterConfiguration] = {}
        ) -> None:
        super().__init__()

        # store readers if they are passed into the constructor or else intialize new list
        self.readers: Mapping[str, ReaderConfiguration] = readers
        # store writers if they are passed into the constructor or else intialize new list
        self.writers: Mapping[str, WriterConfiguration] = writers
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
            raise ConfigurationError('dabapush project could not acquire a dabapush configuration')
        # get constructor from registry
        pinst = self.configuration.get_reader(type)(name)
        self.readers[name] = pinst

        # return id
        return pinst.id

    def remove_reader(self, name: str) -> None:
        if name in self.readers:
            self.readers.pop(name)

    def list_readers(self) -> List[dict]:
        # copy stuff
        return [
            value for value in self.readers.values()
        ]

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