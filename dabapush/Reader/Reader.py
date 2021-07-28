from pathlib import Path
import abc

class Reader(object):

    path: Path

    def __init__(self, path: Path):
        self.path = path

        @abc.abstractmethod
        def read(self):
            return
