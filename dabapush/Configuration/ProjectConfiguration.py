import yaml
from typing import List, Dict
from .ConfigurationError import ConfigurationError
from .Configuration import Configuration
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


class ProjectConfiguration(yaml.YAMLObject):
    """
    ProjectConfiguration hold necessary configuration informations
    
    
    A PojectConfiguration is for reading and writing data as well as the project's meta data
    e.g. author name(s) and email addresses.

    Attributes:
        readers (Dict[str, ReaderConfiguration]): Dict of ReaderConfigurations 
        writers (Dict[str, WriterConfiguration]): Dict of WriterConfigurations
    """

    def __init__(
        self,
        readers: Dict[str, ReaderConfiguration] = {},
        writers: Dict[str, WriterConfiguration] = {}
    ) -> None:
        """Initialize a ProjectConfiguration with optional arguments"""
        super().__init__()

        # store readers if they are passed into the constructor or else intialize new list via default arg
        self.readers: Dict[str, ReaderConfiguration] = readers
        # store writers if they are passed into the constructor or else intialize new list via default arg
        self.writers: Dict[str, WriterConfiguration] = writers
        # the global and/or local configurations are sepratedly stored objects and are, thus,
        # not deserialized and requiere further setup in our class, see property `self.is_initialized`
        # and method `self.initialize()`.
        self.configuration: Configuration = None

    def __repr__(self) -> str:
        return super().__repr__()

    def add_reader(self, type: str, name: str) -> None:
        '''add a reader configuration to the project

        Args:
            self (ProjectConfiguration):
                selfy-self
            type (str):
                name of the configuration to add
            name (str):
                name given to the configuration
        Returns:
            None:
        Raises:
            ConfigurationError: ff no local or global configurations are found
        '''
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
        ''' remove a reader from the configuration
        '''
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