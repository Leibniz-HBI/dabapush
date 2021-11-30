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
  
    # PROJECT specific methods
    def pr_init():
        """
        Initliaze a new project in the current directory
        """
        pass
    def pr_write():
        """
        Write the current configuration to the project configuration file in the current directory
        """
        pass
    def pr_read():
        """
        Read the project configuration file in the current directory
        """
        pass
       
    # READER specific methods
    def rd_add():
        """
        add a reader to the current project
        """
        pass
    def rd_rm():
        """
        remove a reader from the current configuration
        """
        pass
    def rd_update():
        """
        update a reader's configuration
        """
        pass

    # WRITER specific methods
    def wr_add():
        """
        add a reader to the current project
        """
        pass
    def wr_rm():
        """
        remove a reader from the current configuration
        """
        pass
    def wr_update():
        """
        update a reader's configuration
        """
        pass

    # JOB specific methods
    def jb_run():
        """
        run the job configured in the current directory
        """
        pass
    def jb_update():
        """
        update the current job's targets
        """
        pass
    