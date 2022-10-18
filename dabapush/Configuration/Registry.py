"""fetching plug-ins from entrypoints and helper methods"""

from importlib.metadata import entry_points
from typing import Any, List, Optional

from .ReaderConfiguration import ReaderConfiguration
from .WriterConfiguration import WriterConfiguration


class Registry:
    """receive plug-ins from entry point"""

    readers = entry_points()["dabapush_readers"]
    writers = entry_points()["dabapush_writers"]

    # --- static methods --- #

    @staticmethod
    def get_reader(name: str) -> Optional[ReaderConfiguration]:
        """
        params:
          name: str:
            registry key to retrieve
        returns:
            ReaderConfiguration or None: the requested ReaderConfiguration or None if
            no matching configuration is found.
        """
        candidates = Registry.readers.select(name=name)
        try:
            return candidates[0].load()
        except IndexError:
            return None

    @staticmethod
    def get_writer(name: str) -> Optional[WriterConfiguration]:
        """
        params:
          name: str:
            registry key to retrieve
        returns:
            WriterConfiguration or None: the requested WriterConfiguration or None if
            no matching configuration is found."""
        candidates = Registry.writers.select(name=name)
        try:
            return candidates[0].load()
        except IndexError:
            return None

    @staticmethod
    def __ensure_reader__(arg: Any) -> bool:
        return issubclass(arg, ReaderConfiguration)

    @staticmethod
    def __ensure_writer__(arg: Any) -> bool:
        return issubclass(arg, WriterConfiguration)

    @staticmethod
    def list_all_readers() -> List[str]:
        """return a list of all readers"""
        return [_.name for _ in Registry.readers]

    @staticmethod
    def list_all_writers() -> List[str]:
        """return a list of all writers"""
        return [_.name for _ in Registry.writers]
