from loguru import logger as log
from pathlib import Path
from .Writer import Writer
import json


class NdjsonWriter(Writer):
    """ """
    
    def __init__(self):
        super().__init__()

    def persist(self, chunkSize: int):
        """

        Args:
          chunkSize: int: 

        Returns:

        """

        last_row = self.buffer.head(chunkSize)
        self.buffer.drop(last_row.index, inplace=True)

        log.info(f'Persisted {len(last_row)} records')
        
        with self.path.open('a') as file:
            last_row.replace(r'\n|\r', r'\\n', regex=True, inplace=True)
            last_row[self.schema].to_json(file, orient="records", lines=True)
        return len(last_row)
