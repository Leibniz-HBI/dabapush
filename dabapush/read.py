from sys import path
from pathlib import Path
from typing import Generator
from loguru import logger as log

def read(path: str, pattern: str, recursive: bool) -> Generator[Path, None, None]:
    """

    Args:
      path: str: 
      pattern: str: 
      recursive: bool: 

    Returns:

    """
    log.info(f'I will read here: {path}')
    
    _path = Path(path).resolve()
    return _path.rglob(pattern) if (recursive == True) else _path.glob(pattern)
