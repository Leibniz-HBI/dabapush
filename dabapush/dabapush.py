from logging import ERROR
from pathlib import Path
import importlib
import click
import sys
import yaml
import multiprocessing.dummy as mp
from multiprocessing import cpu_count
from loguru import logger as log

from .read import read
from .writer import writer

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--pattern', default='*.json', help='file extension to look for')
@click.option('--host', default='localhost', help='Host address of the dabase too write to.')
@click.option('--port', default='5432', help='Host port of the dabase-server.')
@click.option('--dbname', default='dabapushed', help='Name of the dabase too write to.')
@click.option('--n_workers', default=cpu_count, help="Number of worker threads to read/write data")
@click.option('--reader', default='Twacapic', help='python class to read stuff (see docs). Possible values: Twacapic')
@click.option('--writer', help='python class to write stuff (see docs)')
@click.option('--recursive', '-r', help='should the reader recurse in subdirectories? Default: TRUE.', is_flag=True)
@click.option('--logfile', help='file to logi in (optional)')
@click.option('--loglevel', default='INFO', help='the level to log, yk')
def run(
    input: str,
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
    # load config
    config = yaml.load(Path('config.yml').open(), Loader=yaml.FullLoader)
    
    log.debug('Using this configuration', config)
    
    # Validate all inputs
    if logfile is not None:
        log.add(logfile, level=loglevel, rotation="64 MB")
        log.add(sys.stderr, level='ERROR')

    log.add('errors.log', level='ERROR')
    log.add('warnings.log', level='WARNING')

    log.info(f'{input}**/*.{pattern} will be written to {host}:{port}/{dbname} with {n_workers} parallel threads')

    ReaderClass = None
    # Load the reader:
    if (reader is not None and reader in config['plugins']['reader'].keys()):
        log.debug(f'Using this reader: {reader}')
        try:
            moduleName = config['plugins']['reader'][reader]['moduleName']
            className = config['plugins']['reader'][reader]['className']
            ReaderClass = importlib.import_module(moduleName, package='dabapush').__getattribute__(className)
        except Exception as e:
            log.error(e)
    else:
        log.warning(f'Reader {reader} cannot be found')

    # Fire up the engines and find in all matching files
    files = read(input, pattern, recursive=recursive)

    def proop(thing: Path) -> any:
        readerInstance = ReaderClass(thing)
        log.debug(f'Reading {thing}')

        return readerInstance.read()
        
    with mp.Pool(int(n_workers)) as pool:
        data = pool.map(proop, files, chunksize=1)
        print(data)

    # start $n_workers workers to read the data
    # if JSON accecssor is given, apply it to each loaded file
    # writer(host, port, dbname)

if __name__ == '__main__':
    run()