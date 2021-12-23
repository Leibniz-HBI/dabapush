from pathlib import Path
from json import load
from typing import Dict
import pandas as pd
from loguru import logger as log
from .Reader import Reader
from ..Configuration.ReaderConfiguration import ReaderConfiguration
class TwacapicReaderConfiguration(ReaderConfiguration):

    yaml_tag = '!dabapush:TwacapicReaderConfiguration'

    def __init__(self, name, id=None, read_path: Path = ...) -> None:
        super().__init__(name, id=id, read_path=read_path)

    def __repr__(self) -> str:
        return super().__repr__()

class TwacapicReader(Reader):
    """ """

    @staticmethod
    def setup(path: Path) -> None:
        """

        Args:
          path: Path: 

        Returns:

        """
        # what did I want do here?
        return
   
    @staticmethod
    def getSchema() -> list(str):
        """

        Args:
          ) -> list(str: 

        Returns:

        """
        if (TwacapicReader.__setup == False):
            raise 'Tryed to use TwacapicReader without setting it up first'
        if (TwacapicReader.config is None):
            raise 'Tryed to use TwacapicReader without proper configuration'
        return [""]

    def __init__(
            self,
            path: Path,
            property: str = 'data'
        ):
        super().__init__(path)
        self.property = property
    
    def read(self):
        """ """
        schema = TwacapicReader.getSchema()
        data = None
        with self.path.open('r') as file:
            try:
                data = load(file)['data']
            except Exception as e:
                log.error(e)
        data = pd.json_normalize(data)
        log.debug(f'Found {len(data)} records in {str(self.path)}')
        return data
