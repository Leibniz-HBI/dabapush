from pathlib import Path
from ujson import load
from typing import Generator

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from .Reader import Reader
from ..utils import unpack, safe_access, flatten

class TwacapicReader(Reader):
    """Reader to read ready to read Twitter json data.
    It matches files in the path-tree against the pattern and reads all files as JSON.
        
    """
    def __init__(
            self,
            config: 'TwacapicReaderConfiguration'
        ):
        """
        Parameters
        ----------
        config: TwacapicReaderConfiguration
            Configuration with all the values TwacapicReader needs for it's thang.
        """
        super().__init__(config)
    
    def read(self) -> Generator[dict, None, None]:
        """reads the configured path a returns a generator of single posts.
        Under normal circumstances you don't need to call this function as everything is handle by `dabapush.Dabapush`.
        This Reference here is added for completeness sake.

        Returns
        -------
        type: Generator[dict, None, None]
        """

        for i in Path(self.config.read_path).rglob(self.config.pattern):
            with i.open() as file:
                res = load(file)

            data = safe_access(res, ['data'])
            includes = safe_access(res, ['includes'])

            if data is not None:
                for post in data:
                    user = unpack(post['author_id'], safe_access(res, ['includes','users']), 'id')
                    if user is not None:
                        post['user'] = user
                        yield flatten(post)
            if includes is not None:
                if 'tweets' in res['includes']:
                    for post in res['includes']['tweets']:
                        user = unpack(post['author_id'], res['includes']['users'], 'id')
                        if user is not None:
                            post['user'] = user
                        yield flatten(post)

class TwacapicReaderConfiguration(ReaderConfiguration):
    """Reader configuration for reading Twacapic's Twitter JSON files."""

    yaml_tag = '!dabapush:TwacapicReaderConfiguration'
    """internal tag for pyYAML
    """

    def __init__(self, name, id=None, read_path: str = None, pattern: str = '*.json') -> None:
        """
        Parameters
        ----------
        name: str
            target name for that instance
        id: UUID
            ID of the instance (default value = None, is set by super class)
        read_path: str
            path to the data directory
        pattern: str
            file pattern to match file names against (default value = '*.json')

        """
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)

    def __repr__(self) -> str:
        return super().__repr__()

    def get_instance(self) -> TwacapicReader:
        """From this method `dabapush.Dabapush` will create the reader instance.
        
        Returns
        -------
        type: TwacapicReader
        """
        return TwacapicReader(self)
