from pathlib import Path
from string import Template
from datetime import datetime
from .WriterConfiguration import WriterConfiguration

class FileWriterConfiguration(WriterConfiguration):
    """Abstract class describing configuration items for a file based writer.
    
    Attributes
    ----------
    path : str, default: '.'

    name_template : str : default: '${date}_${time}_${name}.${type}'
        Template string for file name creation, the above four keys are available by default.
        Other data can be passed into str.Template by passing the `additional_keys` parameter into `make_file_name`.
    """
    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: str = '.',
        name_template: str = "${date}_${time}_${name}.${type}"
    ) -> None:
        """
        Parameters
        ----------
        name : str
            target pipeline name
        id : UUID
            instance UUID
        chunk_size : int, default : 2000
        """
        super().__init__(name, id=id, chunk_size=chunk_size)

        self.path = path
        self.name_template = name_template

    def make_file_name(self, additional_keys: dict = {}) -> str:
        """

        Parameters
        ----------
        additional_keys : dict
            Pass in a dict to allow for other data in the templating string (Default value = {})

        Returns
        -------
        type : str
            New file name as specified by the templating string

        """
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
        """

        Parameters
        ----------
        template : str



        Returns
        -------

        """
        self.name_template = template
