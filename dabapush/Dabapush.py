from loguru import logger as log
from pathlib import Path

class Dabapush(object):
    """ This is the main class for this application.

    It is a Singleton pattern class and follows the interface pattern as well.
    
    
    """

    __instance__ = None

    def __new__(
        cls,
        working_dir: Path = Path()
    ):
        if (cls.__instance__ is None):
            cls.__instance__ = super(Dabapush, cls).__new__(cls)
            # init code here: ...
            cls.__instance__.working_dir = working_dir
        return cls.__instance__

    def update_reader_targets(self, name: str) -> None:
        pass
