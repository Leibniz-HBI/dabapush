import abc
from ..Configuration.ReaderConfiguration import ReaderConfiguration

class Reader(abc.ABC):
    """ Abstract base class for all reader plugins. BEWARE: readers and writers are never
    to be instanced directly by the user but rather will be obtain by calling
    `get_instance()` on their specific Configuration-counterparts.
    """

    def __init__(self, config: ReaderConfiguration):
        self.config = config

    @abc.abstractmethod
    def read(self):
        """ """
        return
