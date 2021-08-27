from .PlugInConfiguration import PlugInConfiguration

class WriterConfiguration(PlugInConfiguration):
    """ """
    def __init__(self, name, id=None) -> None:
        super().__init__(name, id=id)