import pandas as pd
import abc
from loguru import logger as log

class Writer(object):
    
    buffer: pd.DataFrame
    chunkSize: int

    # TODO: get chunksize from config
    def __init__(self):
        self.buffer = pd.DataFrame()
        self.chunkSize = 100

    def write(self, df: pd.DataFrame):
        self.buffer = pd.concat([self.buffer, df], ignore_index=True, sort=False)
        self.__writeHandler()
 
    def __writeHandler(self):
        log.info(f'Buffer now contains {len(self.buffer)} records.')
        # Call write persistance loop to empty buffer
        while (len(self.buffer) > self.chunkSize):
            self.persist()

    @abc.abstractmethod
    def persist(self) -> None:
        return None
    