from pathlib import Path
import pathlib
import importlib
from typing import Dict, Literal
import click
import sys
import yaml
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from threading import get_ident
from loguru import logger as log
from .read import read

@click.command()
@click.argument('input', type=click.Path(path_type=pathlib.Path))
@click.option('--pattern', default='*.json', help='file extension to look for')
@click.option('--host', default='localhost', help='Host address of the dabase too write to.')
@click.option('--port', default='5432', help='Host port of the dabase-server.')
@click.option('--dbname', default='dabapushed', help='Name of the dabase too write to.')
@click.option('--n_workers', default=cpu_count, help="Number of worker threads to read/write data")
@click.option('--reader', default='Twacapic', help='python class to read stuff (see docs). Possible values: Twacapic')
@click.option('--writer', default='CSV',help='python class to write stuff (see docs)')
@click.option('--recursive', '-r', help='should the reader recurse in subdirectories? Default: TRUE.', is_flag=True)
@click.option('--logfile', help='file to logi in (optional)')
@click.option('--loglevel', default='INFO', help='the level to log, yk')
def run(
    input: Path,
    pattern: str,
    reader: str,
    writer: str,
    host: str,
    port: str,
    dbname: str,
    n_workers: str,
    recursive: bool,
    logfile: str,
    loglevel: str
):
    # guard against non-existent read directory
    if not input.exists():
        log.error('input directory must exist')
        exit(128)
    if not input.is_dir():
        log.error('input must be a directory')
        exit(128)

    # inititalize file tracking
    touched_path = Path()/'.dabapush.touched.yml'
    touched = yaml.safe_load(touched_path.open('r')) \
        if touched_path.exists() \
        else []
    
    # load config
    config_path = Path()/'config.yml'
    config = None
    with config_path.open() as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    if config is None:
        raise
    print(config)
    log.remove()
    log.add(sys.stdout, level=loglevel)
    log.debug('Using this configuration', config)
    # Validate all inputs
    if logfile is not None:
        log.add(logfile, level=loglevel, rotation="64 MB")
        log.add(sys.stderr, level='ERROR')

    log.add('errors.log', level='ERROR')
    log.add('warnings.log', level='WARNING')

    log.info(f'{input}**/*.{pattern} will be written to {host}:{port}/{dbname} with {n_workers} parallel threads')

    ReaderClass = None
    # Load the reader/writer:
    ReaderClass = load_from_config(reader, 'reader', config)
    WriterClass = load_from_config(writer, 'writer', config)

    # Fire up the engines and find in all matching files
    files = read(input, pattern, recursive=recursive)

    # Get a Writer
    writerInstance = WriterClass()

    def proop(thing: Path) -> any:
        if str(thing) not in touched:
            readerInstance = ReaderClass(thing)
            log.debug(f'Reading {thing}')
            touched.append(str(thing))
            return writerInstance.write(readerInstance.read())
        
    with ThreadPoolExecutor() as executor:
        # log.debug(f'Starting {active_count()} threads.')
        lines = executor.map(proop, files)
        # log.info(f'Read a total of {sum(lines)} records')

    with touched_path.open('w') as file:
        yaml.dump(touched,file)

def load_from_config(name: str, key: str, config: Dict):
    if (name is not None and name in config['plugins'][key].keys()):
        log.debug(f'Using this {key}: {name}')
        ReaderClass = None
        try:
            moduleName = config['plugins'][key][name]['moduleName']
            className = config['plugins'][key][name]['className']
            ReaderClass = importlib.import_module(moduleName, package='dabapush').__getattribute__(className)
        except Exception as e:
            log.error(e)
        return ReaderClass
    else:
        log.warning(f'{key.upper()} {name} cannot be found')
    # start $n_workers workers to read the data
    # if JSON accecssor is given, apply it to each loaded file
    # writer(host, port, dbname)

if __name__ == '__main__':
    run()
