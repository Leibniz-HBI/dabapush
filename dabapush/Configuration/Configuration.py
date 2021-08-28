import yaml
from typing import ChainMap, Dict, List
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration

class Configuration(yaml.YAMLObject):
    yaml_tag = '!dabapush:Configuration'
    _instances = []

    """ """
    def __init__(
        self,
        readers: Dict[str, str] = {},
        writers: Dict[str, str] = {}
    ) -> None:
        super().__init__()

        self.readers = readers
        self.writers = writers


        Configuration._instances.append(self)

    def __del__(self):
        Configuration._instances.remove(self)

    def __repr__(self) -> str:
        return super().__repr__()

    @staticmethod
    def get_reader(type: str) -> ReaderConfiguration or None:
        """

        Args:
          type: str: 

        Returns:

        """
        a = [inst.readers for inst in Configuration._instances]
        readers = ChainMap(*a)

        if type in readers:
            # TODO: look up ReaderConfiguration subclasses from registered plugins
            return ReaderConfiguration

    @staticmethod
    def get_writer(type: str) -> WriterConfiguration or None:
        """

        Args:
          type: str: 

        Returns:

        """
        a = [inst.writers for inst in Configuration._instances]
        writers = ChainMap(*a)

        if type in writers:
            # TODO: look up WriterConfiguration subclasses from registered plugins
            return WriterConfiguration

    def register_reader(self, name: str, plugin_configuration) -> None:
        """

        Args:
          name: str: 
          constructor: 

        Returns:

        """
        if self.__ensure_reader__(plugin_configuration):
            self.readers[name] = plugin_configuration

    def register_writer(self, name: str, constructor) -> None:
        """

        Args:
          name: str: 
          constructor: 

        Returns:

        """
        pass

    def remove_reader(self, name: str) -> bool:
        """

        Args:
          name: str: 

        Returns:

        """
        pass

    def remove_writer(self, name: str) -> bool:
        """

        Args:
          name: str: 

        Returns:

        """
        pass

    def list_writers(self) -> List[str]:
        """ """
        pass

    def list_writers(self) -> List[str]:
        """ """
        pass

    def merge_with(conf: 'Configuration') -> 'Configuration':
        """

        Args:
          conf: 'Configuration': 

        Returns:

        """
        pass
    
    def __ensure_reader__(self, arg: any) -> bool:
        # TODO: this is a stun function, which _shopuld_ ensure that
        # things passed in here are actually ReaderConfigurations _OR_
        # classes that inherit from that.
        return True
        
    def __ensure_writer__(self, arg: any) -> bool:
        # TODO: this is a stun function, which _shopuld_ ensure that
        # things passed in here are actually ReaderConfigurations _OR_
        # classes that inherit from that.
        return True
