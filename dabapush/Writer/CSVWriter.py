import csv
from loguru import logger as log
from pathlib import Path
from .Writer import Writer

class CSVWriter(Writer):
    
    def __init__(self):
        super().__init__()

    def persist(self, chunkSize: int):
        self.buffer,last_row=self.buffer.drop(self.buffer.tail(chunkSize).index),self.buffer.tail(chunkSize)
        log.info(f'Persisted {len(last_row)} records')
        with Path('res.csv').open('a') as file:
            last_row.to_csv(file, index=False)
        return