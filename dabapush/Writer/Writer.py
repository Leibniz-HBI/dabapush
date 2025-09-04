"""Writer base class for writing records to a destination.

The Writer class is an abstract base class for writing records to a destination.
It provides a write method to consume a queue of records and a persist method to
write the records to the destination.
"""

import abc
from pathlib import Path
from typing import Iterator, Set

from ..Configuration.WriterConfiguration import WriterConfiguration
from ..Record import Record


class Writer:
    """Abstract base class for all writer plugins."""

    def __init__(self, config: WriterConfiguration):
        """Initializes the Writer with the given configuration.

        Args:
           config (WriterConfiguration): The configuration for the writer.
        """
        super().__init__()

        self.config = config
        # initialize file log

        # TODO(@pekasen): is this still needed?
        self.log_path = Path(f".dabapush/{config.name}.jsonl")

    @abc.abstractmethod
    def write(self, queue: Iterator[Record]) -> Set[str] | None:
        """Abstract method to persist the records to the destination.
        Subclasses **must** implement this method.

        Args:
            record_batch (List[Record]): Items to be consumed.
        Returns:
            error_set: set of record uuids which failed to be written.
        """

    @property
    def name(self):
        """Gets the name of the writer.

        Returns:
            str: The name of the writer.
        """
        return self.config.name

    @property
    def id(self):
        """Gets the ID of the writer.

        Returns:
            str: The ID of the writer.
        """
        return self.config.id
