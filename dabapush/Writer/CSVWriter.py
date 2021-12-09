from loguru import logger as log
from pathlib import Path
from .Writer import Writer

class CSVWriter(Writer):
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
        
        # TODO: make path configurable!!!
        with self.path.open('a') as file:
            last_row.replace(r'\n|\r', r'\\n', regex=True, inplace=True)
            last_row[self.schema].to_csv(file, index=False, header=False)
        return len(last_row)
