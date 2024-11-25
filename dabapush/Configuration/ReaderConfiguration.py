"""Reader Interface.
"""

from abc import ABC

from .PlugInConfiguration import PlugInConfiguration

# pylint: disable=W0622


class ReaderConfiguration(PlugInConfiguration, ABC):
    """Abstract Base class for all ReaderConfigurations."""

    yaml_tag = "!dabapush:ReaderConfiguration"

    def __init__(self, name, id, read_path: str or None, pattern: str or None) -> None:
        super().__init__(name, id=id)
        self.read_path = read_path if read_path is not None else "."
        self.pattern = pattern if pattern is not None else "*.json"
