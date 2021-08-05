from pathlib import Path
from json import load
import pandas as pd
from loguru import logger as log
from .Reader import Reader

class TwacapicReader(Reader):
    
    def __init__(self, path: Path, property: str = 'data'):
        super().__init__(path)
        self.property = property
    
    def read(self):
        data = None
        with self.path.open('r') as file:
            try:
                data = load(file)['data']
            except Exception as e:
                log.error(e)
        data = pd.json_normalize(data)
        log.debug(f'Found {len(data)} records in {str(self.path)}')
        return data