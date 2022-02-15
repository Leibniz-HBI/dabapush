from loguru import logger as log
from pathlib import Path
from .Writer import Writer
from ..Configuration.FileWriterConfiguration import FileWriterConfiguration

class CSVWriterConfiguration(FileWriterConfiguration):
    type = "CSV" # static property of CSVWriterConfiguration

    def __init__(self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: Path = Path()
    ) -> None:
        super().__init__(name, id=id, chunk_size=chunk_size, path=path)

       
    @property
    def file_path(self) -> Path:
        # evalutate self.name_template
        file_name = self.make_file_name()
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
