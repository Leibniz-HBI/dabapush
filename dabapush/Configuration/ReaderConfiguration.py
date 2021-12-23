from pathlib import Path
from .PlugInConfiguration import PlugInConfiguration

class ReaderConfiguration(PlugInConfiguration):
    """ """

    type = 'UNSET'

    def __init__(self, name, id, read_path: Path or None) -> None:
        super().__init__(name, id=id)
        self.read_path = read_path if read_path is not None else Path()

    def __repr__(self) -> str:
        return super().__repr__()