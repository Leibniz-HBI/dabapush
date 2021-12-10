from .PlugInConfiguration import PlugInConfiguration

class WriterConfiguration(PlugInConfiguration):
    """ """
    def __init__(self, name, id=None, chunk_size: int = 2000) -> None:
        super().__init__(name, id=id)
        
        self.chunck_size = chunk_size