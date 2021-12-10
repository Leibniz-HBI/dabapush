from pathlib import Path
from string import Template
from datetime import datetime
from .WriterConfiguration import WriterConfiguration

class FileWriterConfiguration(WriterConfiguration):

    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: Path = Path(),
        name_template: str = "$date_$time_$name.$type"
    ) -> None:
        super().__init__(name, id=id, chunk_size=chunk_size)

        self.path = path
        self.name_template = Template(name_template) # template for string interpolation for the filename

    def make_file_name(self):
        now = datetime.now()
        return self.name_template.substitute(
            ** {
                "date": datetime.strftime(now, '%Y-%m-%d'),
                "time": datetime.strftime(now, '%H%M'),
                "name": self.name,
                "id": self.id,
                "type": self.type
            }
        )