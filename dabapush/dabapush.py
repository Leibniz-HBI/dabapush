from pathlib import Path
import pathlib
from importlib_metadata import entry_points, EntryPoint
from typing import Dict
import click
import sys
import yaml
from multiprocessing import cpu_count
from concurrent.futures import ThreadPoolExecutor
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

    # Load the reader/writer:
    reader_class = load_from_config(reader, 'reader', config)
    writer_class = load_from_config(writer, 'writer', config)

    if reader_class is None or writer_class is None:
        log.error("Error in loading plugins. Aborting.")
        sys.exit(127)

    # Fire up the engines and find in all matching files
    files = read(input, pattern, recursive=recursive)

    # Get a Writer
    writer_instance = writer_class()

    def proop(thing: Path) -> any:
        if str(thing) not in touched:
            reader_instance = reader_class(thing)
            log.debug(f'Reading {thing}')
            touched.append(str(thing))

            return writer_instance.write(reader_instance.read())
    lines = [proop(_) for _ in files]
    # with ThreadPoolExecutor() as executor:
    #     # log.debug(f'Starting {active_count()} threads.')
    #     lines = executor.map(proop, files)
    #     # log.info(f'Read a total of {sum(lines)} records')
    log.info(f"Processed {len(lines)} files.")
    with touched_path.open('w') as file:
        yaml.dump(touched,file)

def load_from_config(name: str, key: str, config: Dict):
    plugins = entry_points(group='dabapush077')
    
    res: list[EntryPoint] = [x for  x in plugins if x.name == name]
    print('plugins:', res)
    if len(res) == 1:
        log.debug(f"Loading {name}.")
        return res[0].load()
    else:
        log.warning(f'{key.upper()} {name} cannot be found')
        return
