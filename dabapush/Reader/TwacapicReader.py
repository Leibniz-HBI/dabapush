"""Read Twitter API v2 response objects"""

# pylint: disable=R,W0622,E0611

from typing import Any, Dict, Generator, List, Optional

from loguru import logger as log
from ujson import load, loads

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..utils import flatten, safe_access, safe_write, unpack
from .Reader import Reader


class TwacapicReader(Reader):
    """Reader to read ready to read Twitter json data.
    It matches files in the path-tree against the pattern and reads all files as JSON.

    Attributes
    ----------
    config: NDJSONRreaderConfiguration
        The configuration file used for reading
    """

    def __init__(self, config: "TwacapicReaderConfiguration"):
        """
        Parameters
        ----------
        config: TwacapicReaderConfiguration
            Configuration with all the values TwacapicReader needs for it's thang.
        """
        super().__init__(config)

    def unpack_tweet(  # pylint: disable=W0102
        self,
        tweet: Dict,
        includes: Dict,
        keys: List[str] = ["media", "user", "entities.mentions"],
    ):
        """unpack tweets"""

        possible_keys = ["media", "user", "entities.mentions"]
        targets = {
            "user": {
                "tweet_id_field": "author_id",
                "tweet_path": [],
                "includes_id_field": "id",
                "includes_field": "users",
                "target_path": ["user"],
                "multiple": False,
            },
            "media": {
                "tweet_id_field": None,
                "tweet_path": ["attachments", "media_keys"],
                "includes_id_field": "media_key",
                "includes_field": "media",
                "target_path": ["media"],
                "multiple": True,
            },
            "entities.mentions": {
                "tweet_id_field": "username",
                "tweet_path": ["entities", "mentions"],
                "includes_id_field": "username",
                "includes_field": "users",
                "target_path": ["entities", "mentions"],
                "multiple": True,
            },
        }

        def handle_item(job_item, job):
            tweet_id_field: str or None = job["tweet_id_field"]
            id = job_item[tweet_id_field] if tweet_id_field is not None else job_item
            if id is None:
                raise f"id cannot be None in {job} and {job_item}"
            includes_key = safe_access(job, ["includes_field"])
            if includes_key not in includes:
                log.warning(f"key not present in additional information dict in: {job}")
                return
            return unpack(id, includes[includes_key], job["includes_id_field"])

        for key in keys:
            if key in possible_keys:
                job = targets[key]
                multiple = job["multiple"]

                path = job["tweet_path"]
                if path is None:
                    raise Exception(f"Accessor path cannot be empty in {job}")
                # see if we'd expect a list
                if multiple is True:
                    job_list: List[Any] or None = safe_access(tweet, path)
                    if job_list is None or len(job_list) == 0:
                        continue
                    value = [handle_item(_, job) for _ in job_list]
                else:
                    job_item = safe_access(tweet, path)
                    if job_item is None:
                        continue
                    value = handle_item(job_item, job)
                if isinstance(value, list):
                    value = [_ for _ in value if _ is not None]
                if value is None or len(value) == 0:
                    log.warning(f"Tweet rejoining failed for {tweet} in job: {job}")
                    continue
                safe_write(tweet, job["target_path"], key=None, value=value)
        log.debug(f"Parsed tweet: {tweet}")
        return tweet

    def read(self) -> Generator[dict, None, None]:
        """reads the configured path a returns a generator of single posts.
        Under normal circumstances you don't need to call this function as
        everything is handle by `dabapush.Dabapush`.

        Returns
        -------
        type: Generator[dict, None, None]
        """

        config: TwacapicReaderConfiguration = self.config

        for i in self.files:
            with i.open() as file:
                if config.lines and config.lines is True:
                    _res = (loads(line) for line in file)
                else:
                    _res = [load(file)]
                for res in _res:

                    data = safe_access(res, ["data"])
                    includes = safe_access(res, ["includes"])

                    if data is not None:
                        for post in data:
                            post = self.unpack_tweet(post, includes)
                            yield flatten(post)
                    if includes is not None and config.emit_references is True:
                        if "tweets" in includes:
                            for post in includes["tweets"]:
                                post = self.unpack_tweet(post, includes)
                                yield flatten(post)


class TwacapicReaderConfiguration(ReaderConfiguration):
    """Reader configuration for reading Twacapic's Twitter JSON files."""

    yaml_tag = "!dabapush:TwacapicReaderConfiguration"
    """internal tag for pyYAML
    """

    def __init__(
        self,
        name,
        id=None,  # pylint: disable=W0622
        read_path: Optional[str] = None,
        pattern: str = "*.json",
        lines=False,
        emit_references=False,
    ) -> None:
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

        self.lines = lines
        self.emit_references = emit_references

    def get_instance(self) -> TwacapicReader:  # pylint: disable=W0221
        """From this method `dabapush.Dabapush` will create the reader instance.

        Returns
        -------
        type: TwacapicReader
        """
        return TwacapicReader(self)
