from pathlib import Path
from typing import Iterator
from loguru import logger as log

def read(path:Path, pattern: str, recursive: bool) -> Iterator[Path]:
    log.info(f'I will read here: {path}')

    _path = Path(path).resolve()
    return _path.rglob(pattern) if (recursive is True) else _path.glob(pattern)
