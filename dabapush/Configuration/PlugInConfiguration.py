import yaml
from uuid import UUID, uuid4

class PlugInConfiguration(yaml.YAMLObject):
    """ """
    
    yaml_tag = '!dabapush:PluginConfiguration'

    type = "NONE"

    def __init__(self, name: str, id: str or None) -> None:
        super().__init__()

        self.name = name
        self.id = id if id is not None else str(uuid4())

    def __repr__(self) -> str:
        return super().__repr__()