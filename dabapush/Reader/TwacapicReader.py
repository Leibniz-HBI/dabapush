import json
from pathlib import Path
from ujson import load
from typing import Dict, Generator
import pandas as pd
from loguru import logger as log
from .Reader import Reader
from ..Configuration.ReaderConfiguration import ReaderConfiguration
class TwacapicReaderConfiguration(ReaderConfiguration):

    yaml_tag = '!dabapush:TwacapicReaderConfiguration'

    def __init__(self, name, id=None, read_path: Path = None) -> None:
        super().__init__(name, id=id, read_path=read_path)

    def __repr__(self) -> str:
        return super().__repr__()

class TwacapicReader(Reader):
    """ """
    def __init__(
            self,
            config: TwacapicReaderConfiguration
        ):
        super().__init__(config)
    
    def join(self, id: str, includes: list[any], id_key: str) -> any or None:
        """
        looks up an entity in a array of dicts by given key.
        """
        for included in includes:
            if id == included[id_key]:
                return included

    def read(self) -> Generator[any]:
        """
        reads the configured path a returns a generator of single posts
        """

        for i in self.config.read_path.rglob(self.config.pattern):
            with i.open() as file:
                res = load(file)

            if 'data' in res:
                for post in res['data']:
                    user = self.join(post['author_id'], res['includes']['includes'], 'id')
                    if user is not None:
                        post['user'] = user
                    yield post
                if 'includes' in res:
                    if 'tweets' in res['includes']:
                        for post in res['includes']['tweets']:
                            user = self.join(post['author_id'], res['includes']['users'], 'id')
                            if user is not None:
                                post['user'] = user
                            yield post
