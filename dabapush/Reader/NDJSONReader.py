from pathlib import Path
import ujson
from typing import Generator

from .Reader import Reader
from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..utils import flatten

class NDJSONReader(Reader):
    """Reader to read ready to read NDJSON data.
    It matches files in the path-tree against the pattern and reads all files and all lines in these file as JSON.
    
    Attributes
    ----------
    config: NDJSONRreaderConfiguration
        The configuration file used for reading
    """

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
    """Read new line delimited JSON files.
    
    Attributes
    ----------
    flatten_dicts: bool
        wether to flatten those nested dictioniaries
    
    """

    yaml_tag = '!dabapush:NDJSONReaderConfiguration'
    """internal tag for pyYAML
    """

    def __init__(
        self,
        name,
        id=None,
        read_path: str = '.',
        pattern:str = '*.ndjson',
        flatten_dicts = True
    ) -> None:
        """
        Parameters
        ----------
        name: str
            target pipeline name
        id : UUID
            ID of the instance (default value = None, is set by super class)
        read_path: str
            path to directory to read
        pattern: str
            filename pattern to match files in `read_path` against
        flatten_dicts: bool
            whether nested dictionaries are flattend (for details see `dabapush.utils.flatten`)

        """
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)
        self.flatten_dicts = flatten_dicts

    def __repr__(self) -> str:
        return super().__repr__()

    def get_instance(self) -> NDJSONReader:
        """Get a configured instance of NDJSONReader
        
        Returns
        -------
        type: NDJSONReader
            Configured instance of NDJSONReader
        """
        return NDJSONReader(self)
