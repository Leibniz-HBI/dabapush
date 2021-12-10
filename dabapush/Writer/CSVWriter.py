from loguru import logger as log
from pathlib import Path
from .Writer import Writer
from ..Configuration.WriterConfiguration import WriterConfiguration

class CSVWriterConfiguration(WriterConfiguration):
    type = "CSV" # static of CSVWriterConfiguration

    def __init__(self, name, id=None, chunk_size: int = 2000, path: Path = Path()) -> None:
        super().__init__(name, id=id)
        
        self.chunk_size = chunk_size
        self.path = path
        self.name_template # template for string interpolation for the filename

    @property
    def file_path(self) -> Path:
        # evalutate self.name_template
        file_name = self.name_template
        # append to self.path and return
        return self.path / file_name

class CSVWriter(Writer):
    """ """
    
    def __init__(self, config: CSVWriterConfiguration):
        super().__init__()
        self.config = config

    def persist(self):
        """

        Args:

        Returns:

        """

        last_row = self.buffer.head(self.config.chunk_size)
        self.buffer.drop(last_row.index, inplace=True)

        log.info(f'Persisted {len(last_row)} records')
        
        # TODO: make path configurable!!!
        with self.config.file_path.open('a') as file:
            last_row.replace(r'\n|\r', r'\\n', regex=True, inplace=True)
            last_row[self.schema].to_csv(file, index=False, header=False)
        return len(last_row)
