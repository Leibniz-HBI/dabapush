from typing import Generator
import pandas as pd
import abc
from loguru import logger as log
from ..Configuration.WriterConfiguration import WriterConfiguration

class Writer(object):
    """ """

    # TODO: get chunksize from config
    def __init__(self, config: WriterConfiguration):
        super().__init__()

        self.config = config
        self.buffer = []

    def __del__(self):
        # flush buffer before destruction
        self.persist()

    def write(self, queue: Generator[any, any, any]):
        """

        Args:
          df: dict

        Returns:

        """
        for item in queue:
            self.buffer.append(item)
            if len(self.buffer) >= self.config.chunck_size:
                self.persist()

    @abc.abstractmethod
    def persist(self) -> None:
        """

        Args:
   
        Returns:

        """
        pass

    @property
    def name(self):
        return self.config.name

    @property
    def id(self):
        return self.config.id