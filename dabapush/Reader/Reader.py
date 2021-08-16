from pathlib import Path
import abc
from typing import Dict

class Reader(object):
    
    config: Dict
    workingPath: Path
    __setup = False

    @staticmethod
    def setup(path: Path) -> None:
        """
        This hook is called by programm start up in order to load additional resources and/or configuration from the working folder.
        Implementation here serves solely as an interface and guideline for implmentation in subclasses.

        Never call this static method from your class definition to set `__setup` to true!
        """
        raise "You shall not call me, understand!"
        Reader.workingPath = Path
        Reader.config = read(path)
        Reader.__setup = True
        return

    def __init__(self, path: Path):
        self.path = path

    @abc.abstractmethod
    def read(self):
        return
