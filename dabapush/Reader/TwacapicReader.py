from pathlib import Path
from pytest import Instance
from ujson import load
from typing import Generator
from loguru import logger as log

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from .Reader import Reader

class TwacapicReader(Reader):
    """
    Reader to read ready to read Twitter json data
    """
    def __init__(
            self,
            config: 'ReaderConfiguration'
        ):
        super().__init__(config)
    
    def join(self, id: str, includes: list[any], id_key: str) -> any or None:
        """
        looks up an entity in a array of dicts by given key.
        """
        for included in includes:
            if id == included[id_key]:
                return included

    def read(self) -> Generator[any, any, any]:
        """
        reads the configured path a returns a generator of single posts
        """

        def safe_access(thing: dict, path: list[str]):
            def safety(thing: dict, attr: str) -> any or None:
                if attr in thing:
                    return thing[attr]
            res = thing
            for attr in path:
                res = safety(res, attr)
                if res is None:
                    break
            return res
        
        def iterate_tweets():
            pass

        for i in Path(self.config.read_path).rglob(self.config.pattern):
            with i.open() as file:
                res = load(file)

            data = safe_access(res, ['data'])
            includes = safe_access(res, ['includes'])

            if data is not None:
                for post in data:
                    user = self.join(post['author_id'], safe_access(res, ['includes','users']), 'id')
                    if user is not None:
                        post['user'] = user
                        yield post
            if includes is not None:
                if 'tweets' in res['includes']:
                    for post in res['includes']['tweets']:
                        user = self.join(post['author_id'], res['includes']['users'], 'id')
                        if user is not None:
                            post['user'] = user
                        yield post

class TwacapicReaderConfiguration(ReaderConfiguration):
    """ Reader configuration for reading Twacapic's Twitter JSON files.
    """

    yaml_tag = '!dabapush:TwacapicReaderConfiguration'

    def __init__(self, name, id=None, read_path: str = None, pattern: str = '*.json') -> None:
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)

    def __repr__(self) -> str:
        return super().__repr__()

    def get_instance(self) -> TwacapicReader:
        return TwacapicReader(self)
