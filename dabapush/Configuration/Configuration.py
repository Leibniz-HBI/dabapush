from pathlib import Path
from typing import ChainMap, List
from dabapush.Reader.Reader import Reader
from dabapush.Writer.Writer import Writer
import yaml
import collections
class Configuration(yaml.YAMLObject):
    def __init__(self, readers: ChainMap[str, Reader] = collections.ChainMap(), writers: ChainMap[str, Writer] = collections.ChainMap()) -> None:
        super().__init__()

        self.readers = readers
        self.writers = writers

    def __repr__(self) -> str:
        return super().__repr__()

    def get_reader(self, type: str) -> Reader:
        pass

    def get_writer(self, type: str) -> Writer:
        pass

    def register_reader(self, name: str, constructor) -> None:
        pass

    def register_writer(self, name: str, constructor) -> None:
        pass

    def remove_reader(self, name: str) -> bool:
        pass

    def remove_writer(self, name: str) -> bool:
        pass

    def list_writers(self) -> List[str]:
        return ['a','b','c']

    def list_writers(self) -> List[str]:
        pass

    def merge_with(conf: 'Configuration') -> 'Configuration':
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