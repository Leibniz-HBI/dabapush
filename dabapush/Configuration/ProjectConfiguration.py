import yaml
from copy import copy
from typing import List, Dict
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
        writers: Dict[str, WriterConfiguration] = {},
        author: str = '',
        name: str = ''
    ) -> None:
        """Initialize a ProjectConfiguration with optional reader and/or writer dicts"""
        super().__init__()

        # store readers if they are passed into the constructor or else intialize new list via default arg
        self.readers: Dict[str, ReaderConfiguration] = readers
        # store writers if they are passed into the constructor or else intialize new list via default arg
        self.writers: Dict[str, WriterConfiguration] = writers

        # initialize project metadata
        self.author = author
        self.name   = name

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.readers},{self.writers})'

    def add_reader(self, type: str, name: str) -> None:
        """add a reader configuration to the project

        Args:
          type: str: registry of the configuration to add 
          name: str: name of the configuration to add

        Returns: Nothing.

        Raises:
          ConfigurationError: if no local or global configurations are found

        """
        # get constructor from registry
        pinst = Configuration.get_reader(type)
        if pinst is not None:
            self.readers[name] = pinst(name)
        else:
            raise Exception(f'{type} not found')

    def remove_reader(self, name: str) -> None:
        """remove a reader from the configuration

        Args:
          name: str: name of the reader to be removed

        Returns: Nada.

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
        # get constructor from registry
        pinst = Configuration.get_writer(type)
        if pinst is not None:
            self.writers[name] = pinst(name)
        else:
            raise Exception(f'{type} not found')

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

    def set_name(self, name):
        self.name = name
    
    def set_author(self, author):
        self.author = author

    @property
    def __configuration__(self):
        a = Configuration()
        print(Configuration._instances)
        return a
