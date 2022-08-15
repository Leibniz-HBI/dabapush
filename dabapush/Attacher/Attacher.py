from abc import abstractmethod
from pathlib import Path
from typing import Dict, Iterator

from dabapush.Configuration.PlugInConfiguration import PlugInConfiguration

class Attacher(object):

    def __init__(self, config) -> None:
        
        self.config = config

    @abstractmethod
    def attach() -> Iterator(Dict):
        pass

class FileAttacher(Attacher):

    def attach(self) -> Iterator(Dict):
        return Path(self.config.path).rglob(self.config.pattern)

class FileAttacherConfiguration(PlugInConfiguration):
    
    def __init__(self, name: str, id: str or None, pattern="*.json", path =".") -> None:
        super().__init__(name, id)

        self.pattern = pattern
        self.path    = path
 