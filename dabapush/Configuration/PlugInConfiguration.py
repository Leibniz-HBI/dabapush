import yaml
from uuid import UUID, uuid4
from abc import abstractclassmethod

class PlugInConfiguration(yaml.YAMLObject):
    """ """
    
    yaml_tag = '!dabapush:PluginConfiguration'

    def __init__(self, name: str, id: str or None) -> None:
        super().__init__()

        self.name = name
        self.id = id if id is not None else str(uuid4())

    def __repr__(self) -> str:
        return super().__repr__()

    @abstractclassmethod
    def get_instance(self) -> 'Reader' or 'Writer':
        """ """
        pass