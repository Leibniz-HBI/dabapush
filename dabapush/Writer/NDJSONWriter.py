from pathlib import Path
from string import Template
from loguru import logger as log

from ..Configuration.FileWriterConfiguration import FileWriterConfiguration
from .Writer import Writer
import ujson


class NDJSONWriter(Writer):
    """ """

    def __init__(self, config: "NDJSONWriterConfiguration"):
        super().__init__(config=config)

    def persist(self):
        """ """

        last_rows = self.buffer
        self.buffer = []

        _file: Path = Path(self.config.path) / self.config.make_file_name()

        with _file.open("a", encoding="utf8") as file:
            for row in last_rows:
                ujson.dump(row, file, ensure_ascii=False)
                file.write("\n")
        log.info(f"Persisted {len(last_rows)} records")

        return len(last_rows)


class NDJSONWriterConfiguration(FileWriterConfiguration):
    """ """

    yaml_tag = "!dabapush:NDJSONWriterConfiguration"

    def __init__(
        self,
        name,
        id=None,
        chunk_size: int = 2000,
        path: str = ".",
        name_template: str = "${date}_${time}_${name}.${type}",
    ) -> None:
        super().__init__(name, id, chunk_size, path, name_template)
        self.type = "ndjson"

    def get_instance(self):
        """ """
        return NDJSONWriter(self)

    def __repr__(self) -> str:
        return super().__repr__()
