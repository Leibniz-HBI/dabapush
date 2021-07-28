import pandas as pd
import abc
from loguru import logger as log

class Writer(object):
    
    buffer: pd.DataFrame
    
    def __init__(self):
        self.buffer = pd.DataFrame()

    def write(self, df: pd.DataFrame):
        self.buffer = pd.concat([self.buffer, df], ignore_index=True, sort=False)
        self.__writeHandler()
 
    def __writeHandler(self):
        log.info(f'Buffer now contains {len(self.buffer)} records.')

    @abc.abstractmethod
    def persist(self) -> None:
        return None
    