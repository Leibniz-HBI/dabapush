import yaml
from uuid import UUID, uuid4

class PlugInConfiguration(yaml.YAMLObject):
    """ """

    type = "NONE"

    def __init__(self, name: str, id: UUID or None) -> None:
        super().__init__()

        self.name = name
        self.id = id if id is not None else uuid4()