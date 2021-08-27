import yaml
from uuid import uuid4

class PlugInConfiguration(yaml.YAMLObject):
    def __init__(self) -> None:
        super().__init__()

        self.id = uuid4()