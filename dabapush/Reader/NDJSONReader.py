from pathlib import Path
import ujson
from typing import Generator

from .Reader import Reader
from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..utils import flatten

class NDJSONReader(Reader):
    """ """

    def __init__(self, config: 'NDJSONReaderConfiguration') -> None:
        super().__init__(config)
    
    def read(self) -> Generator[dict, None, None]:
        """reads multiple ndjson files and emits them line by line"""
        for file_path in Path(self.config.read_path).rglob(self.config.pattern):
            with file_path.open('r') as file:
                lines = file.readlines()
                for line in lines:
                    if self.config.flatten_dicts != True:
                        yield ujson.loads(line)
                    else:
                        yield flatten(ujson.loads(line))


class NDJSONReaderConfiguration(ReaderConfiguration):
    """ """

    yaml_tag = '!dabapush:NDJSONReaderConfiguration'

    def __init__(
        self,
        name,
        id=None,
        read_path: str = '.',
        pattern:str = '*.ndjson',
        flatten_dicts = True
    ) -> None:
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)
        self.flatten_dicts = flatten_dicts

    def __repr__(self) -> str:
        return super().__repr__()

    def get_instance(self) -> NDJSONReader:
        """ """
        return NDJSONReader(self)
