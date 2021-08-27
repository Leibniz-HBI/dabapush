import yaml
from typing import Dict, List
from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration
class Configuration(yaml.YAMLObject):
    """ """
    def __init__(
        self,
        readers: Dict[str, str] = {},
        writers: Dict[str, str] = {}
    ) -> None:
        super().__init__()

        self.readers = readers
        self.writers = writers

    def __repr__(self) -> str:
        return super().__repr__()

    def get_reader(self, type: str) -> ReaderConfiguration:
        """

        Args:
          type: str: 

        Returns:

        """
        if type in self.readers:
            # TODO: look up ReaderConfiguration subclasses from registered plugins
            return ReaderConfiguration

    def get_writer(self, type: str) -> WriterConfiguration:
        """

        Args:
          type: str: 

        Returns:

        """
        if type in self.writers:
            # TODO: look up WriterConfiguration subclasses from registered plugins
            return WriterConfiguration

    def register_reader(self, name: str, constructor) -> None:
        """

        Args:
          name: str: 
          constructor: 

        Returns:

        """
        pass

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


# class DabapushConfiguration(object):
#     def __init__(self) -> None:
#         super().__init__()
#         self.plugins: Mapping(str, PluginConfiguration)

# class Configuration(object):

#     def __init__(self, glob_conf: DabapushConfiguration, loc_conf: DabapushConfiguration, wd: Path, sd: Path) -> None:
#         super().__init__()
#         self.glob_conf = glob_conf
#         self.loc_conf = loc_conf
#         self.wd = wd
#         self.sd = sd

# class PluginConfiguration(object):
#     def __init__(self, description: str, module_name: str, class_name: str) -> None:
#         super().__init__()

#         self.description = description
#         self.module_name = module_name
#         self.class_name = class_name