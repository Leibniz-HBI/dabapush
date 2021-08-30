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
    
    # --- static methods --- #

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

    @staticmethod
    def __ensure_reader__(arg: any) -> bool:
        # TODO: this is a stub function, which _should_ ensure that
        # things passed in here are actually ReaderConfigurations _OR_
        # classes that inherit from that.
        return issubclass(arg, ReaderConfiguration)
    
    @staticmethod
    def __ensure_writer__(arg: any) -> bool:
        # TODO: this is a stub function, which _should_ ensure that
        # things passed in here are actually WriterConfigurations _OR_
        # classes that inherit from that.
        return issubclass(arg, WriterConfiguration)
    
    @staticmethod
    def list_all_writers(self) -> List[str]:
        """ """
        pass

    @staticmethod
    def list_all_writers(self) -> List[str]:
        """ """
        pass


    # --- instance methods --- #
    def register_reader(self, name: str, plugin_configuration) -> None:
        """

        Args:
          name: str: 
          constructor: 

        Returns:

        """
        if Configuration.__ensure_reader__(plugin_configuration):
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
    