from pathlib import Path
from ujson import load
from typing import Generator

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from .Reader import Reader
from ..utils import join, safe_access, flatten

class TwacapicReader(Reader):
    """
    Reader to read ready to read Twitter json data
    """
    def __init__(
            self,
            config: 'ReaderConfiguration'
        ):
        super().__init__(config)
    
    def read(self) -> Generator[any, any, any]:
        """
        reads the configured path a returns a generator of single posts
        """

        for i in Path(self.config.read_path).rglob(self.config.pattern):
            with i.open() as file:
                res = load(file)

            data = safe_access(res, ['data'])
            includes = safe_access(res, ['includes'])

            if data is not None:
                for post in data:
                    user = join(post['author_id'], safe_access(res, ['includes','users']), 'id')
                    if user is not None:
                        post['user'] = user
                        yield flatten(post)
            if includes is not None:
                if 'tweets' in res['includes']:
                    for post in res['includes']['tweets']:
                        user = join(post['author_id'], res['includes']['users'], 'id')
                        if user is not None:
                            post['user'] = user
                        yield flatten(post)

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
