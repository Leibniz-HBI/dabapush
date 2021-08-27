import yaml
from copy import copy
from typing import List, Dict
from .ConfigurationError import ConfigurationError
from .Configuration import Configuration
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration

class ProjectConfiguration(yaml.YAMLObject):
    """ProjectConfiguration hold necessary configuration informations
    
    
    A ProjectConfiguration is for reading and writing data as well as the project's meta data
    e.g. author name(s) and email addresses.
    """
    yaml_tag = '!dabapush:ProjectConfiguration'


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
        self.__configuration__: Configuration = None

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.readers},{self.writers})'

    def add_reader(self, type: str, name: str) -> None:
        """add a reader configuration to the project

        Args:
          self(ProjectConfiguration): selfy-self
          type(str): name of the configuration to add
          name(str): 
          type: str: 
          name: str: 

        Returns:

        Raises:
          ConfigurationError: ff no local or global configurations are found

        """
        # check wether global/local configuration is set up
        if (self.is_initialized == True): 
            pass
        else:
            raise ConfigurationError('dabapush project could not acquire a dabapush configuration')
        # get constructor from registry
        pinst = self.__configuration__.get_reader(type)(name)
        self.readers[name] = pinst

        # return id
        return pinst.id

    def remove_reader(self, name: str) -> None:
        """remove a reader from the configuration

        Args:
          name: str: 

        Returns:

        """
        if name in self.readers:
            self.readers.pop(name)

    def list_readers(self) -> List[dict]:
        """list all configured readers

        Returns: List[Dict]: list of dicts with name- and id-fields
        
        """
        # copy stuff
        return [
            value for value in self.readers.values()
        ]

    def add_writer(self, type: str, name: str) -> None:
        """

        Args:
          type: str: 
          name: str: 

        Returns: None: nothing to see, carry on.

        """
        if self.is_initialized == True:
            writer = self.__configuration__.get_writer(type)(name)
            self.writers[name] = writer
            return writer.id
        else:
            raise ConfigurationError('Could not acquire a local/global configuration')

    def remove_writer(self, name: str):
        """

        Args:
          name: str: 

        Returns:

        """
        if name in self.writers:
            self.writers.pop(name)

    def list_writers(self):
        """list all configured writers

        Returns: List[Dict]: list of dicts with name- and id-fields
        
        """
        # copy stuff
        return [
            value for value in self.writers.values()
        ]

    @property
    def is_initialized(self) -> bool:
        """ """
        return self.__configuration__ is not None


    # pass a global/local/merged configuration to the project
    def initialize(self, conf: Configuration) -> None:
        """

        Args:
          conf: Configuration: 

        Returns:

        """
        self.__configuration__ = conf

    def to_yaml(self, path) -> None:
        dumpy = copy(self)
        dumpy.__configuration__= None
        return yaml.dump(dumpy)