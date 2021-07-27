from sys import path
from pathlib import Path
from typing import Generator
from loguru import logger as log

class Reader:
    path: Path

    def __init__(self, path: Path):
        print(f'Hello!')
        self.path = path

def read(path: str, pattern: str) -> Generator[Path, None, None]:
    log.info(f'I will read here: {path}')
    
    _path = Path(path)
    _query = f'{path}/**/*' if (pattern is None) else f'{path}/**/*.{pattern}'
    _files = _path.glob(_query)

    return _files
