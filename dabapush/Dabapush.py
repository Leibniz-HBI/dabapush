from loguru import logger as log

class Dabapush(object):
    """ This is the main class for this application.

    It is a Singleton pattern class and follwos the interface pattern as well.
    
    
    """

    __instance__ = None

    def __new__(
        cls,
        working_dir: Path
    ):
        if (cls.__instance__ is None):
            cls.__instance__ = super(Dabapush, cls).__new__(cls)
            # init code here: ...
        return cls.__instance__
