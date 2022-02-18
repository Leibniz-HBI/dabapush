
import pandas as pd
from loguru import logger as log
from pathlib import Path
from .Writer import Writer
from ..Configuration.FileWriterConfiguration import FileWriterConfiguration

class CSVWriter(Writer):
    """ """
    
    def __init__(self, config: 'CSVWriterConfiguration'):
        super().__init__(config)
        self.config = config
        self.chunk_number = 1

    def persist(self):
        """ """

        last_rows = self.buffer
        self.buffer = []


        log.info(f'Persisted {len(last_rows)} records')
        _path = Path(self.config.path) / self.config.make_file_name({'chunk_number': self.chunk_number})
        pd.DataFrame.\
            from_dict(last_rows).\
            replace(r'\n|\r', r'\\n', regex=True).\
            to_csv(
                _path,
                index=False
            )
        self.chunk_number += 1

        return len(last_rows)

class CSVWriterConfiguration(FileWriterConfiguration):
    """ """

    yaml_tag = '!dabapush:CSVWriterConfiguration'

    def __init__(self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: str = '.',
        name_template: str = "${date}_${time}_${name}_${chunk_number}.${type}"
    ) -> None:
        super().__init__(name, id=id, chunk_size=chunk_size, path=path, name_template=name_template)
        self.type = "csv"
       
    @property
    def file_path(self) -> Path:
        """ """
        # evalutate self.name_template
        file_name = self.make_file_name()
        # append to self.path and return
        return self.path / file_name

    def get_instance(self):
        """ """
        return CSVWriter(self)

    def __repr__(self) -> str:
        return super().__repr__()
