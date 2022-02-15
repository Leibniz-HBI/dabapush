from pathlib import Path
from loguru import logger as log

from ..Configuration.FileWriterConfiguration import FileWriterConfiguration
from .Writer import Writer
import ujson

class NDJSONWriter(Writer):
    """ """
    
    def __init__(self, config: 'NDJSONWriterConfiguration'):
        super().__init__(config=config)

    def persist(self):
        """

        Args:

        Returns:

        """

        last_rows = self.buffer
        self.buffer = []
        
        
        with self.path.open('a') as file:
            for row in last_rows:
                ujson.dump(row, file)
        log.info(f'Persisted {len(last_rows)} records')
        
        return len(last_rows)

class NDJSONWriterConfiguration(FileWriterConfiguration):

    yaml_tag = '!dabapush:NDJSONWriterConfiguration'

    def __init__(self, name, id=None, chunk_size: int = 2000, path: Path = ..., name_template: str = "__.") -> None:
        super().__init__(name, id, chunk_size, path, name_template)

    def get_instance(self):
        return NDJSONWriter(self)
