import abc
from typing import Generator
from ..Configuration.ReaderConfiguration import ReaderConfiguration

class Reader(abc.ABC):
    """Abstract base class for all reader plugins.
    
    **BEWARE**: readers and writers are never to be instanced directly by the user but rather will be obtain by calling
    `get_instance()` on their specific Configuration-counterparts.

    Attributes
    ----------
    config : ReaderConfiguration


    """

    def __init__(self, config: ReaderConfiguration):
        """
        Parameters
        ----------
        config : ReaderConfiguration
            Configuration file for the reader. In concrete classes it will be sub-class of ReaderConfiguration.
        """
        self.config = config

    @abc.abstractmethod
    def read(self) -> Generator[dict, None, None]:
        """Subclasses **must** implement this abstract method and implement their reading logic here.

        Returns
        -------
        type: Generator[dict, None, None]
            Generator which _should_ be one item per element.
        """
        return
