from loguru import logger as log
from pathlib import Path
import os

from .Configuration.ProjectConfiguration import ProjectConfiguration
from .Configuration.Configuration import Configuration

class Dabapush(object):
    """ This is the main class for this application.

    It is a Singleton pattern class and follows the interface pattern as well.
    
    
    """

    __instance__ = None

    def __new__(
        cls,
        working_dir: Path = Path(os.getcwd())
    ):
        if (cls.__instance__ is None):
            inst = super(Dabapush, cls).__new__(cls)
            # init code here: ...
            log.info('Started Dabapush.')
            inst.local_config = None
            inst.global_config = None
            inst.working_dir = working_dir
            inst.source_dir  = Path(__file__).parent.parent
            
            cls.__instance__ = inst
        return cls.__instance__

    def update_reader_targets(self, name: str) -> None:
        pass

    def set_local_config(self, config: ProjectConfiguration) -> None:
        self.local_config = config

    def set_global_config(self, config: Configuration) -> None:
        self.global_config = config