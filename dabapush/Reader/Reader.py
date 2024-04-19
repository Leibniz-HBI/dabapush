"""This module contains the abstract base class for all reader plugins."""

import abc
from pathlib import Path
from typing import Iterator

import ujson
from loguru import logger as log

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record


class Reader(abc.ABC):
    """Abstract base class for all reader plugins.

    **BEWARE**: readers and writers are never to be instanced directly by the user but rather will
    be obtained by calling `get_instance()` on their specific Configuration-counterparts.

    Args:
        config (ReaderConfiguration): The configuration for the reader.
    """

    def __init__(self, config: ReaderConfiguration):
        """
        Parameters
        ----------
        config : ReaderConfiguration
            Configuration file for the reader. In concrete classes it will
            be a subclass of ReaderConfiguration.
        """
        self.config = config
        # initialize file log
        if not Path(".dabapush/").exists():
            Path(".dabapush/").mkdir()

        self.log_path = Path(".dabapush/log.jsonl")

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """
        return

    @property
    def files(self) -> Iterator[Path]:
        """Generator for all files matching the pattern in the read_path."""
        fresh = Path(self.config.read_path).rglob(self.config.pattern)
        old_stock_dir = Path("./.dabapush")
        old_stock = []

        if old_stock_dir.exists() and (old_stock_dir / "log.jsonl").exists():
            with (old_stock_dir / "log.jsonl").open("r") as ff:
                old_stock = [
                    ujson.loads(_) for _ in ff.readlines()  # pylint: disable=I1101
                ]  # pylint: disable=I1101

        return (
            self._log(a)
            for a in (_ for _ in fresh if str(_) not in [f["file"] for f in old_stock])
        )

    def _log(self, file: Path) -> Path:
        with self.log_path.open("a", encoding="utf8") as f:
            ujson.dump(  # pylint: disable=I1101
                {"file": str(file), "status": "read"}, f
            )
            f.write("\n")
            log.debug(f"Done with {str(file)}")
        return file
