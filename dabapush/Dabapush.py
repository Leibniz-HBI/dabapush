from loguru import logger as log
from pathlib import Path
import os

from .Configuration.ProjectConfiguration import ProjectConfiguration
from .Configuration.Configuration import Configuration

import yaml

from .Configuration.Configuration import Configuration
from .Configuration.ProjectConfiguration import ProjectConfiguration

class Dabapush(object):
    """ This is the main class for this application.

    It is a Singleton pattern class and follows the interface pattern as well.
    """

    __instance__ = None

    def __new__(
        cls,
        install_dir: Path = Path(__file__).parent.parent,
        working_dir: Path = Path() # automagically defaults to cwd
    ):
        if (cls.__instance__ is None):
            cls.__instance__ = super(Dabapush, cls).__new__(cls)
            # init code here: ...
            cls.__instance__.working_dir = working_dir
            cls.__instance__.install_dir = install_dir
            # load global config
            cls.__instance__.gc_load()
            if not cls.__instance__.pr_read():
                cls.__instance__.pr_init()
        return cls.__instance__

    def update_reader_targets(self, name: str) -> None:
        pass
  
    # PROJECT specific methods
    def pr_init(self):
        """
        Initliaze a new project in the current directory
        """
        self.config = ProjectConfiguration()
        self.pr_write()

    def pr_write(self):
        """
        Write the current configuration to the project configuration file in the current directory
        """
        if self.config is not None:
            conf_path = self.working_dir / 'dabapush.yml'
            with conf_path.open('w') as file:
                yaml.dump(
                    self.config,
                    file
                )

    def pr_read(self) -> bool:
        """
        Read the project configuration file in the current directory

        returns:
            bool Indicates wether loading load successful
        """
        conf_path = self.working_dir / 'dabapush.yml'
        if conf_path.exists():
            with conf_path.open('r') as file:
                self.config = yaml.full_load(file)
            return True
        else:
            return False

    # READER specific methods
    def rd_add(self, reader: str, name: str):
        """
        add a reader to the current project
        """
        self.config.add_reader(
            reader,
            name
        )

    def rd_rm(self):
        """
        remove a reader from the current configuration
        """
        pass
    def rd_update(self):
        """
        update a reader's configuration
        """
        pass

    # WRITER specific methods
    def wr_add(self):
        """
        add a reader to the current project
        """
        pass
    def wr_rm(self):
        """
        remove a reader from the current configuration
        """
        pass
    def wr_update(self):
        """
        update a reader's configuration
        """
        pass

    # JOB specific methods
    def jb_run(self):
        """
        run the job configured in the current directory
        """
        pass
    def jb_update(self):
        """
        update the current job's targets
        """
        pass
    
    def gc_load(self):
        """
        load the global registry and configuration
        """
        conf_path = self.install_dir / 'config.yml'
        with conf_path.open('r') as file:
            self.global_config = yaml.full_load(file)
        
