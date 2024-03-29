"""CSVWriter, Philipp Kessling, 2022
Leibniz-Institute for Media Research Hamburg
"""

from pathlib import Path

import pandas as pd
from loguru import logger as log

from ..Configuration.FileWriterConfiguration import FileWriterConfiguration
from .Writer import Writer


class CSVWriter(Writer):
    """Writes CSVs from buffered stream"""

    def __init__(self, config: "CSVWriterConfiguration"):
        super().__init__(config)
        self.config = config
        self.chunk_number = 1

    def persist(self):
        """persist buffer to disk"""

        last_rows = self.buffer
        self.buffer = []

        log.info(f"Persisted {len(last_rows)} records")
        _path = Path(self.config.path) / self.config.make_file_name(
            {"chunk_number": self.chunk_number}
        )
        pd.DataFrame(last_rows, dtype=str).replace(r"\n|\r", r"\\n", regex=True).to_csv(
            _path, index=False
        )
        self.chunk_number += 1

        return len(last_rows)


class CSVWriterConfiguration(FileWriterConfiguration):
    """Configuration for the CSVWriter"""

    yaml_tag = "!dabapush:CSVWriterConfiguration"

    def __init__(  # pylint: disable=R0913
        self,
        name,
        id=None,  # pylint: disable=W0622
        chunk_size: int = 2000,
        path: str = ".",
        name_template: str = "${date}_${time}_${name}_${chunk_number}.${type}",
    ) -> None:
        super().__init__(
            name, id=id, chunk_size=chunk_size, path=path, name_template=name_template
        )
        self.type = "csv"

    @property
    def file_path(self) -> Path:
        """get the path to a file to write in"""
        # evalutate self.name_template
        file_name = self.make_file_name()
        # append to self.path and return
        return Path(self.path) / file_name

    def get_instance(self):  # pylint: disable=W0221
        """get configured instance of CSVWriter"""
        return CSVWriter(self)
