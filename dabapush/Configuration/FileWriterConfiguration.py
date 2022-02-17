from pathlib import Path
from string import Template
from datetime import datetime
from .WriterConfiguration import WriterConfiguration

class FileWriterConfiguration(WriterConfiguration):
    """ Abstract class describing configuration items for a file based writer
    """
    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: str = '.',
        name_template: str = "${date}_${time}_${name}.${type}"
    ) -> None:
        super().__init__(name, id=id, chunk_size=chunk_size)

        self.path = path
        self.name_template = name_template

    def make_file_name(self, additional_keys: dict = {}) -> str:
        now = datetime.now()
        return Template(self.name_template).substitute(
            ** {
                "date": datetime.strftime(now, '%Y-%m-%d'),
                "time": datetime.strftime(now, '%H%M'),
                "name": self.name,
                "id": self.id,
                "type": self.type,
                **additional_keys
            }
        )

    def set_name_template(self, template: str):
        self.name_template = template
