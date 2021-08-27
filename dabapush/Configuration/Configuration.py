from pathlib import Path
from typing import Mapping
import yaml

class Configuration(yaml.YAMLObject):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

    



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